Name:           dvdstyler
Version:        1.5.1
Release:        3%{?dist}
Epoch:          1
Summary:        Cross-platform DVD authoring system

Group:          Applications/Multimedia
License:        GPL+
URL:            http://www.dvdstyler.de/
Source0:        http://downloads.sourceforge.net/dvdstyler/DVDStyler-%{version}.tar.gz
Patch0:         %{name}-1.5.1-desktop.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  wxGTK-devel >= 2.6.3
BuildRequires:  wxsvg-devel
BuildRequires:  gettext
BuildRequires:  mpgtx
BuildRequires:  netpbm-progs
BuildRequires:  mjpegtools
BuildRequires:  dvdauthor
BuildRequires:  mkisofs
BuildRequires:  dvd+rw-tools
BuildRequires:  libgnomeui-devel
BuildRequires:  libjpeg-devel
BuildRequires:  desktop-file-utils
Requires:       mpgtx
Requires:       netpbm-progs
Requires:       mjpegtools
Requires:       dvdauthor
Requires:       mkisofs
Requires:       dvd+rw-tools
# Optional, defaults to off in burn settings in 1.5.1
Requires(hint): dvdisaster
# This is not strictly true, but it's the default previewer, and mplayer
# doesn't support DVD menus, so...
Requires:       xine

%description
DVDStyler is a cross-platform DVD menu creation GUI that allows
creation of DVD navigation menus similar to those found on most
commercial DVD's.  It leverages various other open source video
rendering programs to produce the final DVD menu navigation system.


%prep
%setup -q -n DVDStyler-%{version}
%patch0 -p1
# Q'n'd fix for configure/Makefile.in outdatedness in 1.5.1:
(echo all: ; echo install:) > install.win32/Makefile.in


%build
%configure --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/dvdstyler
# Desktop entry and icon are supposed to be installed by "make install"
# in 1.5.1 (to paths we don't want) but are not due to configure/Makefile.in
# and friends outdatedness, watch this space in > 1.5.1.
desktop-file-install --vendor livna --mode 644 \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  data/dvdstyler.desktop
install -Dpm 644 data/dvdstyler.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/dvdstyler.png
%find_lang %{name}


%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_bindir}/dvdstyler
%{_datadir}/dvdstyler/
%{_datadir}/applications/*dvdstyler.desktop
%{_datadir}/icons/hicolor/*x*/apps/dvdstyler.png


%changelog
* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:1.5.1-3
- rebuild

* Wed Aug 22 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.1-2
- License: GPL+
- Sync icon cache scriptlets with Fedora Wiki.

* Mon Jul  9 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5.1-1
- 1.5.1.

* Fri Jun  8 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.5-1
- 1.5.

* Fri May 25 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-8
- Rebuild.

* Tue Feb  6 2007 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-7
- Patch for wxWidgets 2.8.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.4-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-5
- Rebuild.

* Sun Apr  9 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-4
- Actually apply the y4mscaler patch (#904).  Note that for the change to take
  effect, old Jpeg2MpegCmd setting may need to be removed from ~/.dvdstyler.
- Install icon to %%{_datadir}/icons/hicolor.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jun 06 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 1:1.4-0.lvn.3
- Add gcc4-x86_64.patch to fix compile on x86_64

* Sun May 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-0.lvn.2
- Patch default config to use y4mscaler and require it due to changes in
  mjpegtools 1.7.0.

* Wed May 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-0.lvn.1
- 1.4, desktop entry patch applied upstream.
- Patch to fix about dialog crash.

* Sun Jan 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.31-0.lvn.1
- First build.
