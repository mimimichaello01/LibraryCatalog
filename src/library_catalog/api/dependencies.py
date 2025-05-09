from src.library_catalog.repositories.jsonbin_repo import JsonBinBookRepository
from src.library_catalog.repositories.open_library_repo import OpenLibraryRepository
from src.library_catalog.services.jsonbin_service import JsonBinServiceImpl
from src.library_catalog.services.open_library_service import OpenLibraryServiceImpl


def get_jsonbin_repository():
    return JsonBinBookRepository()


def get_openlib_repository():
    return OpenLibraryRepository()


def get_openlib_service():
    return OpenLibraryServiceImpl(repo=get_openlib_repository())


def get_jsonbin_service():
    return JsonBinServiceImpl(
        repo=get_jsonbin_repository(),
        openlib=get_openlib_service()
    )
