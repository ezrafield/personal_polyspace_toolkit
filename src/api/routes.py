from src.services.example_service import ExampleService


def health() -> dict[str, str]:
    service = ExampleService()
    return {"status": service.health_status()}
