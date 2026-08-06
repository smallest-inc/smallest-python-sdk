from typing import TypeVar, Union

T = TypeVar("T")


class NotGiven:
    """
    Sentinel value for unset optional parameters.

    This allows distinguishing between:
    - Parameter not provided at all (NOT_GIVEN)
    - Parameter explicitly set to None
    - Parameter set to an actual value

    Example:
        def func(temp: NotGivenOr[float] = NOT_GIVEN):
            if is_given(temp):
                # temp was explicitly provided
                use_temp(temp)
            else:
                # temp was not provided, use default
                use_default()
    """

    def __bool__(self) -> bool:
        """NotGiven is falsy."""
        return False

    def __repr__(self) -> str:
        return "NOT_GIVEN"


NOT_GIVEN = NotGiven()

NotGivenOr = Union[T, NotGiven]


def is_given(value: NotGivenOr[T]) -> bool:
    """
    Check if a value was explicitly provided (not NOT_GIVEN).

    Args:
        value: The value to check

    Returns:
        True if value is not NOT_GIVEN, False otherwise

    Example:
        >>> is_given(0.7)
        True
        >>> is_given(None)
        True
        >>> is_given(NOT_GIVEN)
        False
    """
    return not isinstance(value, NotGiven)
