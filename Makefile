include /usr/share/i18n/SUPPORTED

INSTALL-SUPPORTED-LOCALES=$(addprefix install-, $(SUPPORTED-LOCALES))

install-locales: $(INSTALL-SUPPORTED-LOCALES)

install-locales-dir:
	mkdir -p $(DESTDIR)/usr/share/locale

$(INSTALL-SUPPORTED-LOCALES): install-locales-dir
	@locale=`echo $@ | sed -e 's/^install-//'`; \
	charset=`echo $$locale | sed -e 's,.*/,,'`; \
	locale=`echo $$locale | sed -e 's,/[^/]*,,'`; \
	input=`echo $$locale | sed 's/\([^.]*\)[^@]*\(.*\)/\1\2/'`; \
	echo "localedef -i $$input -c -f $$charset" \
	     "$(DESTDIR)/usr/share/locale/$$locale"; \
	localedef -i $$input -c -f $$charset \
		     $(DESTDIR)/usr/share/locale/$$locale; \

