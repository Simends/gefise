PREFIX := /

install:
	install -Dm755 gefise.py $(PREFIX)/usr/bin/gefise
	install -Dm644 boot-entries.example.yml $(PREFIX)/etc/boot-entries.example.yml

uninstall:
	rm -f $(PREFIX)/usr/bin/gefise
