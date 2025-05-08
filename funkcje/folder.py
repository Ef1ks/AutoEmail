import os

def create_dir(base_dir):
    attachment_dir = os.path.join(base_dir, 'attachments')
    if not os.path.exists(attachment_dir):
        os.makedirs(attachment_dir, exist_ok=True)
    return attachment_dir