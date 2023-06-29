from dotenv import dotenv_values

class AppEnv():
    def settings():
        config = dotenv_values(".env")

        return {"error":"ddd"}