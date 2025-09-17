from services.Translator.src.config import *
from services.Translator.src.manager import Manager

translator = Manager(TOPIC_PUB, TOPIC_SUB)

def main():
    translator.consume_and_publish_translated_text()

if __name__ == '__main__':
    main()