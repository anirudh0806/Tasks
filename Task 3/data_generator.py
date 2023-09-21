import random
import string

user_ids = list(range(1, 100))
recipient_ids = list(range(1, 100))


def generate_message():
    """
    Generate a random message with user and recipient IDs.

    :return: A dictionary containing user_id, recipient_id, and a random message.
    """
    random_user_id = random.choice(user_ids)

    recipient_ids_copy = recipient_ids.copy()
    # Ensuring that the user_id and recipient_id are not the same
    recipient_ids_copy.remove(random_user_id)
    random_recipient_id = random.choice(recipient_ids_copy)

    # Generating a random message of length 9 which consists of alphabets
    random_message = ''.join(random.choice(
        string.ascii_letters) for i in range(9))

    return {
        'user_id': random_user_id,
        'recipient_id': random_recipient_id,
        'message': random_message
    }


if __name__ == '__main__':
    print(generate_message())
