
    if not os.environ.get('FOLIAGE_WIDGET', None):
        import rumps
        # We are the parent process.
        os.environ['FOLIAGE_WIDGET'] = 'True'
        pid = os.fork()
        if pid == 0:
            # We are the child process.
            print('in child')
            print('b')
            app = rumps.App('Foliage')
            print('starting widget app')
            app.run()
        else:
            os.environ['FOLIAGE_WIDGET'] = str(pid)

