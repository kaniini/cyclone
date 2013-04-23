class IRCMessage:
    def __init__(self, data):
        self._parse(data)

    def _parse(self, input):
        """Parse an IRC message.

        >>> parse(':lol!lol@example.com JOIN #lol')
        ({}, u':lol!lol@example.com', u'JOIN', [u'lol'])
        >>> parse('@foo=bar :lol!lol@example.com PRIVMSG #lol :lol')
        ({u'@foo': u'bar'}, u':lol!lol@example.com', u'PRIVMSG', [u'#lol', u':lol'])
        """
        if isinstance(input, bytes):
            input = input.decode('UTF-8', 'replace')

        string = input.split(' ')

        if string[0].startswith('@'):
            tag_str = string[0][1:].split(',')
            string = string[1:]
            tags = {}

            for tag in tag_str:
                k, v = tag.split('=', 1)
                tags[k] = v
        else:
            tags = {}

        if string[0].startswith(':'):
            prefix = string[0][1:]
            string = string[1:]
        else:
            prefix = None

        verb = string[0].upper()
        args = string[1:]

        for arg in args:
            if arg.startswith(':'):
                idx  = args.index(arg)
                arg  = ' '.join(args[idx:])
                arg  = arg[1:]
                args = args[:idx]

                args.append(arg)

                break

        self.tags = tags
        self.source = prefix
        self.verb = verb
        self.args = args

    def args_str(self):
        base = []
        for arg in self.args:
            if ' ' not in arg:
                base.append(arg)
            else:
                base.append(':%s' % (arg))
                break

        return ' '.join(base)

    def __str__(self):
        if self.tags:
            tags = ['%s=%s' % (k, v) for k, v in self.tags.items()]
            tags = '@%s ' % (','.join(tags))
        else:
            tags = ''

        if self.source:
            source = ':%s ' % (self.source)
        else:
            source = ''

        verb = self.verb

        args = self.args_str()

        return ''.join((tags, source, verb, ' ', args))
