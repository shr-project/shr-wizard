MAINTAINERCLEANFILES = Makefile.in
MODULE = wizard
MODULE_ARCH="$host_os-$host_cpu-$release"

AM_CFLAGS = -Wall @ENLIGHTENMENT_CFLAGS@

pkgdir                 = $(libdir)/enlightenment/modules/$(MODULE)/$(MODULE_ARCH)
pkg_LTLIBRARIES        = page_300.la

page_300_la_SOURCES      = page_300.c
page_300_la_LIBADD       = @ENLIGHTENMENT_LIBS@ @dlopen_libs@
page_300_la_LDFLAGS      = -module -avoid-version

uninstall:
	rm -rf $(DESTDIR)$(libdir)/enlightenment/modules/$(MODULE)/page_300.*