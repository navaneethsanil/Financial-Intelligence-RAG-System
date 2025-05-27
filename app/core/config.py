from pydantic import BaseSettings


class Settings(BaseSettings):
    # App metadata
    APP_NAME: str = "Financial-Intelligence-Rag-System"
    DEBUG: bool = False

    # Database configuration
    DB_HOST: str
    DB_USER: str
    DB_PASS: str

    # Pinecone configuration
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    INDEX_NAME: str

    # OpenAI configuration
    OPENAI_API_KEY: str

    class Config:
        """
        Pydantic configuration class for customizing behavior.

        `env_file` points to the .env file from which environment variables should be loaded.
        """

        env_file = ".env"


# Instantiate settings globally for access throughout the application
settings = Settings()
