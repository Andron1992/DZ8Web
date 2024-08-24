
from models import Author, Quote
from config import connect_to_db


def search_by_name(name):
    authors = Author.objects(fullname__icontains=name)
    if not authors:
        print(f"No authors found with name containing '{name}'")
        return


    for author in authors:
        quotes = Quote.objects(author=author)
        if quotes:
            print(f"Quotes by {author.fullname}:")
            for quote in quotes:
                print(f"- {quote.quote}")
        else:
            print(f"No quotes found for author: {author.fullname}")


def main():
    connect_to_db()

    while True:
        command = input("Enter command (name:, tag:, tags:, exit): ").strip()

        if command.startswith("name:"):
            name = command.split(":")[1].strip()
            search_by_name(name)

        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = Quote.objects(tags__icontains=tag)
            if quotes:
                print(f"Quotes with tag '{tag}':")
                for quote in quotes:
                    print(f"- {quote.quote}")
            else:
                print(f"No quotes found with tag: {tag}")

        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(',')
            quotes = Quote.objects(tags__in=tags)
            if quotes:
                print(f"Quotes with tags {', '.join(tags)}:")
                for quote in quotes:
                    print(f"- {quote.quote}")
            else:
                print(f"No quotes found with tags: {', '.join(tags)}")

        elif command == "exit":
            break

        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
