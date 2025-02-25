from fastapi import APIRouter, UploadFile, File, HTTPException
from api.aws.s3 import s3_client, AWS_BUCKET_NAME, AWS_REGION
from botocore.exceptions import BotoCoreError, ClientError

router = APIRouter()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()  # Read file contents
        print(f"File received: {file.filename}, Size: {len(contents)} bytes")
        
        # Reset file pointer before passing to S3
        file.file.seek(0)

        s3_client.upload_fileobj(
            file.file,
            AWS_BUCKET_NAME,
            file.filename,
        )

        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "fileUrl": file_url,
        }
    except Exception as e:
        return {"error": str(e)}
    
@router.get("/profile-pic/{filename}")
async def get_image(filename: str):
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_BUCKET_NAME, "Key": filename},
            ExpiresIn=3600,
        )
        return {"fileUrl": url}
    except Exception as e:
        return {"error": str(e)}
    
@router.delete("/delete-profile-pic/{filename}")
async def delete_image(filename: str):
    try:
        s3_client.delete_object(Bucket=AWS_BUCKET_NAME, Key=filename)
        return {"message": "File deleted successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
    
@router.put("/update-profile-pic/{filename}")
async def update_file(filename: str, file_obj: UploadFile = File(...), bucket: str = AWS_BUCKET_NAME):
    try:
        # Check if the file exists in S3
        s3_client.head_object(Bucket=bucket, Key=filename)

        # Upload the new file (overwrite the existing one)
        s3_client.upload_fileobj(file_obj.file, bucket, filename, ExtraArgs={"ContentType": file_obj.content_type})

        # Generate the new file URL
        file_url = f"https://{bucket}.s3.{AWS_REGION}.amazonaws.com/{filename}"
        return {"message": "File updated successfully", "file_url": file_url}

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found in bucket '{bucket}'")
        else:
            raise HTTPException(status_code=500, detail=f"S3 error: {str(e)}")

    except BotoCoreError as e:
        raise HTTPException(status_code=500, detail=f"AWS Boto3 error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
