from src.api.users import scramble


def test_password_scramble():
    # Create a sample password for testing
    password = "qVk*fv:}7LUEcVa7m"

    # Hash the password using the scramble function
    hashed_password = scramble(password)

    # Verify that the hashed password is different from the original password
    assert password != hashed_password