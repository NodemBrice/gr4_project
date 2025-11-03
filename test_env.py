from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()  # Loads from .env in current dir

    # Print with masking for sensitive info
    def mask(value):
        if value:
            return value[:4] + "****" + value[-4:]
        return "Not set"

    print("OPENAI_KEY:", mask(os.getenv("OPENAI_API_KEY")))
    print("SMTP_SERVER:", os.getenv("SMTP_SERVER", "Not set"))
    print("SMTP_USER:", os.getenv("SMTP_USER", "Not set"))
    print("FROM_EMAIL:", os.getenv("FROM_EMAIL", "Not set"))
    print("ADMIN_EMAIL:", os.getenv("ADMIN_EMAIL", "Not set"))