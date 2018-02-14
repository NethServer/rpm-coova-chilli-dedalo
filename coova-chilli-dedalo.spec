Summary:   Coova-Chilli patched version for Dedalo
Name:      coova-chilli-dedalo
Version:   1.4
Release:   1%{?dist}
URL:       http://coova.github.io/
Source0:   https://github.com/NethServer/coova-chilli/archive/master.tar.gz
License:   GPL
Provides:  coova-chilli
Conflicts: coova-chilli

# Needed for sh bootstrap, build phase
BuildRequires: autoconf automake libtool libcurl-devel c-ares-devel gengetopt gcc-c++

%if %{!?_without_ssl:1}0
BuildRequires: openssl-devel
%endif

# Require haserl since the internal captive portal uses it, like all other CPs for chilli I'm aware of at the moment.
Requires: haserl libcurl c-ares

%if 0%{?rhel} >= 7
# In RH7, json-c is in a stock rpm
Requires: json-c
BuildRequires: json-c-devel
%endif

%description

Coova-Chilli is a fork of the ChilliSpot project - an open source captive
portal or wireless LAN access point controller. It supports web based login
(Universal Access Method, or UAM), standard for public HotSpots, and it
supports Wireless Protected Access (WPA), the standard for secure roamable
networks. Authentication, Authorization and Accounting (AAA) is handled by
your favorite radius server. Read more at http://coova.github.io/.

%prep
%setup -n coova-chilli-master

%build
sh bootstrap
%configure \
        --disable-static \
        --enable-shared \
	--enable-largelimits \
	--enable-miniportal \
	--enable-chilliredir \
	--enable-chilliproxy \
        --enable-chilliscript \
	--enable-ipwhitelist \
	--with-poll \
	--with-curl \
%if 0%{?rhel} >= 7
    --with-json \
    --enable-json \
%else
    --enable-libjson \
%endif
%if %{!?_without_ssl:1}0
	--with-openssl \
	--enable-chilliradsec \
%endif


make

%install
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_prefix}/include/*
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a

# Place a default config file to be edited by the admin
cp -p %{buildroot}%{_sysconfdir}/chilli/defaults %{buildroot}%{_sysconfdir}/chilli/config
# throw away the initial comments telling to copy the defaults to config
perl -ni -e '1 .. /^\s*$/ and /^#/ or print' %{buildroot}%{_sysconfdir}/chilli/config
perl -ni -e '1 ... /^\S/ and /^\s*$/ or print' %{buildroot}%{_sysconfdir}/chilli/config
# Remove unused init scripts
rm -rf  %{buildroot}/etc/init.d/

%check
rm -f %{buildroot}%{_libdir}/python/*.pyc
rm -f %{buildroot}%{_libdir}/python/*.pyo

%clean
rm -rf %{buildroot}
make clean

%post

%preun

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*.so*
%{_libdir}/python/CoovaChilliLib.py
%doc AUTHORS COPYING ChangeLog INSTALL README doc/dictionary.coovachilli doc/hotspotlogin.cgi
%doc doc/fmttxt.pl doc/attributes doc/chilli.conf doc/firewall.* doc/freeradius.users doc/hotspotlogin* doc/*.php
%config %{_sysconfdir}/chilli.conf
%config %{_sysconfdir}/chilli/gui-config-default.ini
%config(noreplace) %{_sysconfdir}/chilli/defaults
%config(noreplace) %{_sysconfdir}/chilli/config
%dir %{_sysconfdir}/chilli
%dir %{_sysconfdir}/chilli/www
%attr(4750,root,root)%{_sbindir}/chilli_script
%config(noreplace) %{_sysconfdir}/chilli/www/*
%config(noreplace) %attr(755,root,root)%{_sysconfdir}/chilli/www/config.sh
%{_sysconfdir}/chilli/wwwsh
%config(noreplace) %{_sysconfdir}/chilli/functions
%config(noreplace) %{_sysconfdir}/chilli/*.sh
%config(noreplace) %{_sysconfdir}/chilli/wpad.dat
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%changelog
