#!/usr/bin/env make -f

ifeq "$(ECHO)" ""
	ECHO=echo
endif

ifeq "$(LINK)" ""
	LINK=ln -sf
endif


ifeq "$(MAKE)" ""
	MAKE=make
endif

ifeq "$(INSTALL)" ""
	INSTALL=install
	ifeq "$(INST_OWN)" ""
		INST_OWN=-o root -g staff
	endif
	ifeq "$(INST_OPTS)" ""
		INST_OPTS=-m 755
	endif
endif

ifeq "$(LOG)" ""
	LOG=no
endif

ifeq "$(LOG)" "no"
	QUIET=@
endif

PHONY: must_be_root

build:
	$(QUIET)$(ECHO) "No need to build. Try make -f Makefile install"

init:
	$(QUIET)$(ECHO) "$@: Done."

install: /usr/local/bin/ /var/lib/restart_service_handler/ must_be_root
	$(QUITE)$(INSTALL) $(INST_OWN) $(INST_OPTS) ./code/restart_service.py /var/lib/restart_service_handler/restart_service.py
	$(QUITE)$(LINK) /var/lib/restart_service_handler/restart_service.py /usr/local/bin/restart_service.py
	$(QUITE) $(WAIT)
	$(QUITE)$(INSTALL) $(INST_OWN) $(INST_OPTS) ./code/__init__.py /var/lib/restart_service_handler/__init__.py
	$(QUITE) $(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

uninstall:
	$(QUITE)unlink /usr/local/bin/restart_service.py 2>/dev/null || true
	$(QUITE)rm -vfR /var/lib/restart_service_handler/ 2>/dev/null || true
	$(QUITE) $(WAIT)
	$(QUIET)$(ECHO) "$@: Done."

purge: clean uninstall
	$(QUIET)$(ECHO) "$@: Done."

test:
	$(QUIET)coverage erase
	$(QUIET)coverage run -p --source=code -m unittest discover --verbose -s ./tests -t ./ || python3 -m unittest discover --verbose -s ./tests -t ./ || python -m unittest discover --verbose -s ./tests -t ./ || DO_FAIL=exit 2 ;
	$(QUIET)coverage combine 2>/dev/null || true
	$(QUIET)coverage report 2>/dev/null || true
	$(QUIET)python3 -m unittest discover --verbose -t ./ || python -m unittest discover --verbose -t ./
	$(QUIET)$(ECHO) "$@: Done."

clean:
	$(QUIET)$(MAKE) -C ./docs/ -f Makefile clean 2>/dev/null || true
	$(QUIET)rm -f tests/*.pyc 2>/dev/null || true
	$(QUIET)rm -f code/*.pyc 2>/dev/null || true
	$(QUIET)rm -f *.pyc 2>/dev/null || true
	$(QUIET)rm -f *.DS_Store 2>/dev/null || true
	$(QUIET)rm -f *~ 2>/dev/null || true
	$(QUIET)rm -f ./*/*~ 2>/dev/null || true
	$(QUIET)rm -f ./.coverage* 2>/dev/null || true
	$(QUIET)rm -f *.DS_Store 2>/dev/null || true
	$(QUIET)rm -f ./*/*.DS_Store 2>/dev/null || true
	$(QUIET)$(ECHO) "$@: Done."

must_be_root:
	runner=`whoami` ; \
	if test $$runner != "root" ; then echo "You are not root." ; exit 1 ; fi

/var/lib/restart_service_handler/: /var/lib/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) "$@" 2>/dev/null
	$(QUITE)$(WAIT)

/usr/local/bin/: /usr/local/ must_be_root
	$(QUITE)$(INSTALL) -d $(INST_OWN) $(INST_OPTS) "$@" 2>/dev/null || true
	$(QUITE)$(WAIT)

%:
	$(QUIET)$(ECHO) "No Rule Found For $@" ; $(WAIT) ;

