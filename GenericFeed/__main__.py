from GenericFeed.main import GenericFeed

if __name__ == '__main__':
    try:
        GenericFeed().run()
    except KeyboardInterrupt:
        print('\n\nExiting...')
        exit(0)
