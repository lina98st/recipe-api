from src.api.users import scramble


def test_password_scramble():
    # Create a sample password for testing
    password = "qVk*fv:}7LUEcVa7m"

    # Hash the password using the scramble function
    hashed_password = scramble(password)

    # Verify that the hashed password is different from the original password
    assert password != hashed_password


def test_random_salt():
    # Create a sample password for testing
    password = "AKzX@Jv_tE2B,maJQ"

    # Generate two hashes from the same password
    hashed_password = scramble(password)
    hashed_password2 = scramble(password)

    # Verify that a new random salt creates a different hash each time
    assert hashed_password != hashed_password2