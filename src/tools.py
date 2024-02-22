from typing import Any, Optional, Sized, Type, TypeVar

T = TypeVar('T')
SizedT = TypeVar('SizedT', bound=Sized)


def require_type(item: T, item_type: Type[Any], message: Optional[str] = None) -> T:
    if message is not None:
        assert isinstance(item, item_type), message
    else:
        assert isinstance(item, item_type)

    return item


def require_not_null(item: Optional[T], message: Optional[str] = None) -> T:
    if message is not None:
        assert item is not None, message
    else:
        assert item is not None

    return item


def require_not_empty(item: SizedT, message: Optional[str] = None) -> SizedT:
    if message is not None:
        assert len(item) != 0, message
    else:
        assert len(item) != 0

    return item
