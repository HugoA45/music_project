from google.cloud import storage
import io

def download_checkpoint_as_file_object(bucket_name, checkpoint_file_name,path):
    """Download a checkpoint file from Google Cloud Storage and return it as a file object.

    Args:
    bucket_name (str): Name of the Google Cloud Storage bucket.
    checkpoint_file_name (str): Name of the checkpoint file in the bucket.

    Returns:
    file: A file-like object of the downloaded checkpoint.
    """

    client = storage.Client()
    bucket = client.bucket(bucket_name)

    blob = bucket.blob(checkpoint_file_name)
    blob.download_to_filename(path)

    print(f"Downloaded {checkpoint_file_name}.")


if __name__ == "__main__":
    model_best_file = download_checkpoint_as_file_object('music_project_bucket', 'model_best.ckpt', 'model_best.ckpt')
    pretrain_model_file = download_checkpoint_as_file_object('music_project_bucket', 'pretrain_model.ckpt', 'pretrain_model.ckpt')



#from google.cloud import storage
#
#def download_checkpoint_to_local_path(bucket_name, checkpoint_file, local_path):
#    """Download a checkpoint file from Google Cloud Storage and save it locally.
#
#    Args:
#    bucket_name (str): Name of the Google Cloud Storage bucket.
#    checkpoint_file (str): Name of the checkpoint file in the bucket.
#    local_path (str): Local path where the file will be saved.
#
#    Returns:
#    str: The local path where the file is saved.
#    """
#    client = storage.Client()
#    bucket = client.bucket(bucket_name)
#
#    blob = bucket.blob(checkpoint_file)
#    blob.download_to_filename(local_path)
#
#    print(f"Downloaded {checkpoint_file} to {local_path}")
#    return local_path
