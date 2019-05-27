#For git snapshots, set to 0 to use release instead:
%global usesnapshot 0
%if 0%{?usesnapshot}
%global commit0 1c9ce4ca75ca5819e50f0728beb0b65959821940
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global snapshottag .git%{shortcommit0}
%endif

%global prerel_real .beta3
%global prerel b2
%global wxsvg_ver 1.5.17

Name:           dvdstyler
Epoch:          2
Version:        3.1
%if 0%{?usesnapshot}
Release:        6.beta4%{?snapshottag}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        Cross-platform DVD authoring application
License:        GPLv2+
URL:            http://www.dvdstyler.de/

# checkout instructions
# git clone git://git.code.sf.net/p/dvdstyler/DVDStyler dvdstyler
# or
# git clone https://git.code.sf.net/p/dvdstyler/DVDStyler dvdstyler
# cd dvdstyler
# git rev-parse --short HEAD
# git archive --format=tar --prefix=dvdstyler/ %%{shortcommit0}
#   -o dvdstyler-%%{shortcommit0}.tar
# bzip2 dvdstyler-%%{shortcommit0}.tar

%if 0%{?usesnapshot}
Source0:        %{name}-%{shortcommit0}.tar.bz2
%else
Source0:        http://downloads.sourceforge.net/dvdstyler/DVDStyler-%{version}.tar.bz2
%endif

Patch1:         dvdstyler-wxwin.m4.patch
Patch2:         ffmpeg35_buildfix.patch
# build
BuildRequires:  automake autoconf
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  byacc
# libraries
BuildRequires:  wxGTK3-devel >= 3.0
# wxsvg version with wxGTK3
BuildRequires:  wxsvg-devel >= %{wxsvg_ver}
BuildRequires:  ffmpeg-devel
BuildRequires:  ffmpeg
#BuildRequires:  libgnomeui-devel
# mpeg
BuildRequires:  dvdauthor
# iso/burn
BuildRequires:  pkgconfig(libudev)
BuildRequires:  genisoimage
BuildRequires:  dvd+rw-tools
#images
BuildRequires:  libjpeg-devel
BuildRequires:  libexif-devel
# documentation
BuildRequires:  zip
BuildRequires:  xmlto

BuildRequires:  desktop-file-utils

Requires:       dvd+rw-tools
Requires:       dvdauthor
Requires:       mjpegtools
Requires:       genisoimage
# wxsvg version with wxGTK3
Requires:       wxsvg >= %{wxsvg_ver}
# note: do not add Require: totem-backend or another DVD player - see
# RPM Fusion bug 366 for more details

%description
DVDStyler is a cross-platform DVD authoring application that makes possible for
video enthusiasts to create professional-looking DVDs. It allows users to
create navigational DVD menus similar to those found on most commercial DVDs.


%prep
%if 0%{?usesnapshot}
%setup -q -n %{name}
%else
%setup -q -n DVDStyler-%{version}
%endif
%patch1 -p1
#%patch2 -p1
#{__sed} -i 's|_T("xine \\"dvd:/$DIR\\"");|_T("totem \\"dvd://$DIR\\"");|' src/Config.h

# fixes E: script-without-shebang
chmod a-x src/*.{h,cpp}

%build
rm -f install-sh depcomp missing mkinstalldirs compile config.guess config.sub install-sh
rm -f aclocal.m4 Makefile.in
#rm -f m4_ax_cxx_compile_stdcxx.m4 m4_ax_cxx_compile_stdcxx.m4 wxwin.m4
#touch NEWS
./autogen.sh
#sed -i 's/WX_CONFIG_CHECK.\[3.0\]/WX_CONFIG_CHECK([3.0.0]/' configure.ac
#autoreconf -i
#sed -i 's/min_wx_version=3.0/min_wx_version=3.0.0/' configure
%configure \
  --disable-dependency-tracking \
#  %if (0%{?fedora} && 0%{?fedora} < 28)
#  --with-wx-config=/usr/bin/wx-config-3.0-gtk2 \
#  %endif

# docs folder is not smp_mflags safe
make -C docs
%make_build


%install
%make_install

# License docs go to another place
rm -rf %{buildroot}%{_docdir}/%{name}/COPYING

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}


%files -f %{name}.lang
%{_docdir}/%{name}
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_mandir}/*/*.gz

%changelog
* Mon May 27 2019 Martin Gansser <martinkg@fedoraproject.org> - 2:3.1-1
- Update to 2:3.1
- Add epoch to allow update

* Tue Apr 16 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:3.1-6.beta4.git1c9ce4c
- Update to 1:3.1-6.beta4.git1c9ce4c

* Fri Apr 12 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:3.1-5.beta3.gite4968db
- Update to 1:3.1-5.beta3.gite4968db

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:3.1-4.beta3.gite4c6466
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:3.1-3.beta3.gite4c6466
- Rebuilt for wxsvg-1.5.16

* Tue Jan 22 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:3.1-2.beta3.gite4c6466
- Update wxsvg_ver 1.5.15

* Sun Jan 20 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:3.1-1.beta3.gite4c6466
- Update to 1:3.1-1.beta3.gite4c6466

* Tue Dec 25 2018 Sérgio Basto <sergio@serjux.com> - 1:3.0.4-6
- Move to wxGTK3 as request in rfbz#5068

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1:3.0.4-4
- Rebuilt for new ffmpeg snapshot

* Wed Feb 28 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1:3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.4-2
- Rebuilt for ffmpeg-3.5 git

* Sun Nov 26 2017 Sérgio Basto <sergio@serjux.com> - 1:3.0.4-1
- Update to 3.0.4

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.3-6
- Rebuild for ffmpeg update

* Sun Oct 08 2017 Sérgio Basto <sergio@serjux.com> - 1:3.0.3-5
- Fix build on f28+ for compat-wxGTK3-gtk2-devel

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1:3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:3.0.3-3
- Rebuild for ffmpeg update

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1:3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Sérgio Basto <sergio@serjux.com> - 1:3.0.3-1
- Update dvdstyler to 3.0.3

* Tue Sep 27 2016 Sérgio Basto <sergio@serjux.com> - 1:3.0.2-3
- Let try compat-wxGTK3-gtk2, rfbz#4267

* Wed Sep 21 2016 Sérgio Basto <sergio@serjux.com> - 1:3.0.2-2
- Be sure that compiles with wxsvg-devel-1.5.9-2

* Tue Aug 23 2016 Sérgio Basto <sergio@serjux.com> - 1:3.0.2-1
- New upstream release 3.0.2

* Tue Aug 16 2016 Sérgio Basto <sergio@serjux.com> - 1:3.0.2-0.2.beta3
- Remove BR:libgnomeui-devel

* Tue Aug 16 2016 Sérgio Basto <sergio@serjux.com> - 1:3.0.2-0.1.beta3
- Update DVDStyler to 3.0.2beta3

* Mon Aug 15 2016 Sérgio Basto <sergio@serjux.com> - 1:2.9.6-5
- Upstream suggested to use wxGTK 3.x.

* Sun Jul 31 2016 Sérgio Basto <sergio@serjux.com> - 1:2.9.6-4
- mpgtx is not required since 2008 !
- Use %%{buildroot} instead $RPM_BUILD_ROOT 
- Pack all documentation 

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1:2.9.6-3
- Rebuilt for ffmpeg-3.1.1

* Thu Jan 07 2016 Sérgio Basto <sergio@serjux.com> - 1:2.9.6-2
- Add license tag and minor clean up

* Wed Jan 06 2016 Sérgio Basto <sergio@serjux.com> - 1:2.9.6-1
- Update to 2.9.6

* Tue Oct 27 2015 Sérgio Basto <sergio@serjux.com> - 1:2.9.4-1
- Update to 2.9.4
- Drop vender tag
- Use autoreconf instead autogen.sh
- Drop validation desktop patch


* Thu Apr 09 2015 Sérgio Basto <sergio@serjux.com> - 1:2.9.2-1
- Update to 2.9.2

* Sat Jan 24 2015 Sérgio Basto <sergio@serjux.com> - 1:2.8.1-1
- Update to 2.8.1.

* Sun Oct 19 2014 Sérgio Basto <sergio@serjux.com> - 1:2.8-3
- Rebuilt for FFmpeg 2.4.3

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 1:2.8-2
- Rebuilt for FFmpeg 2.4.x

* Mon Sep 15 2014 Sérgio Basto <sergio@serjux.com> - 1:2.8-1
- New upstream release.

* Sun Aug 10 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7.2-4
- Rebuild for new wxsvg

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7.2-3
- Rebuilt for ffmpeg-2.3

* Mon May 12 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7.2-2
- Rebuild for new wxsvg

* Tue Apr 08 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7.2-1
- New upstream release. 
  * fixed some small bugs
  * win32: updated ffmpeg to current snapshot version

* Sat Mar 29 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7.1-2
- Rebuilt for ffmpeg-2.2

* Fri Mar 14 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7.1-1
- New upstream release

* Tue Feb 25 2014 Sérgio Basto <sergio@serjux.com> - 1:2.7-1
- Update to 2.7 
  * better support of multiple titlesets 
  * added a possibility to add a chapter selection menu 
  * added the rectangle selection tool 
  * added possibility to align multiple buttons to left/right/top/bottom 
  * added slide properties dialog 
  * added a possibility to select a titleset to import from DVD 
  * changed to use mplex tool for menu multiplexing 
  * updated ffmpeg to version 2.1.3

* Sat Jan 04 2014 Sérgio Basto <sergio@serjux.com> - 1:2.6.1-2
- New upstream source. 

* Wed Dec 04 2013 Sérgio Basto <sergio@serjux.com> - 1:2.6.1-1
- New upstream release.

* Thu Nov 14 2013 Sérgio Basto <sergio@serjux.com> - 2.6-1
- Update to 2.6 final version.

* Sat Oct 26 2013 Sérgio Basto <sergio@serjux.com> - 2.6-0.1_rc2
- Update to 2.6rc2

* Sun Oct 20 2013 Sérgio Basto <sergio@serjux.com> - 2.5.2-2
- Rebuilt for wxsvg-1.2.1

* Mon Oct 07 2013 Sérgio Basto <sergio@serjux.com> - 2.5.2-1
- Update to 2.5.2

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:2.5-3
- Rebuilt

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:2.5-2
- Rebuilt for FFmpeg 2.0.x

* Sun Jul 14 2013 Sérgio Basto <sergio@serjux.com> - 2.5-1
- New upstream release.

* Sun May 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1:2.4.3-2
- Rebuilt for x264/FFmpeg

* Mon Apr 08 2013 Sérgio Basto <sergio@serjux.com> - 2.4.3-1
- Update to 2.4.3

* Tue Mar 19 2013 Sérgio Basto <sergio@serjux.com> - 2.4.2-1
- New upstream release.

* Wed Feb 20 2013 Sérgio Basto <sergio@serjux.com> - 2.4.1-1
- Update to 2.4.1

* Sat Feb 09 2013 Sérgio Basto <sergio@serjux.com> - 2.4-1
- New upstream release.

* Wed Jan 23 2013 Sérgio Basto <sergio@serjux.com> - 2.4-0.1.rc1
- Update to 2.4rc1, to fix rfbz #2652 and rebuild for new wxSVG.
- drop dvdstyler-wxVillaLib-libjpeg.patch, fixed upstream.

* Wed Dec 26 2012 Sérgio Basto <sergio@serjux.com> - 2.3.5-2
- New upstream source, which have guide_pt and guide_ro.

* Wed Dec 26 2012 Sérgio Basto <sergio@serjux.com> - 2.3.5-1
- New upstream release.
- Added new guide_pt and guide_ro from CVS that was missing in source.
- Minor clean ups

* Sat Nov 24 2012 Sérgio Basto <sergio@serjux.com> - 2.3.4-2
- Rebuild for ffmpeg-libs-1.0

* Thu Nov 22 2012 Sérgio Basto <sergio@serjux.com> - 2.3.4-1
- New upstream release.

* Sun Nov 04 2012 Sérgio Basto <sergio@serjux.com> - 2.3.3-1
- New upstream release.

* Sun Aug 26 2012 Sérgio Basto <sergio@serjux.com> - 2.3-1
- Update upstream release

* Tue Aug 07 2012 Sérgio Basto <sergio@serjux.com> - 2.3-0.1.rc1
- Update upstream release
- Drop patch2 and patch3, seems that was applied in upstream

* Wed Jul 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:2.0-0.5.rc1
- Switch to pkgconfig(libudev)

* Tue Jun 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:2.0-0.4.rc1
- Rebuilt for FFmpeg

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:2.0-0.3.rc1
- Rebuilt for x264/FFmpeg

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1:2.0-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 Stewart Adam <s.adam at diffingo.com> 1:2.0-0.1.rc1
- Update to 2.0rc1

* Wed Sep 28 2011 Stewart Adam <s.adam at diffingo.com> 1:1.8.4.3-1
- Update to 1.8.4.3

* Mon Sep 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 1:1.8.3-2
- Rebuilt for FFmpeg-0.8

* Mon May 2 2011 Stewart Adam <s.adam at diffingo.com> - 1:1.8.3-1
- Update to 1.8.3
- Port changes from F-14 branch

* Sat Oct 24 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.4-1
- Update to 1.7.4

* Wed Oct 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.7.3-0.2.beta3
- rebuild for new ffmpeg

* Fri Jun 19 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.3-0.1.beta3
- Update to 1.7.3 beta3
- Remove gcc44 patch

* Tue Apr 7 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.2-3
- Add patch to fix gcc 4.4-related build errors

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.7.2-2
- rebuild for new F11 features

* Sun Mar 8 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.2-1
- Remove dependency on totem-backend (#366)
- Update to 1.7.2

* Sat Jan 24 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-4
- Remove wxsvg_freeworld patch
- desktop and icon files now install correctly, don't install them manually
- Remove hicolor scriptlets
- Update %%description

* Fri Jan 23 2009 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-3
- Bump for proper upgrade path from F-10

* Thu Dec 11 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-2
- Remove previous link hacks and link against wxsvg_freeworld
- Use totem to preview DVDs
- Don't require dvdisaster; it's optional
- Fix changelog dates wrt epoch

* Thu Nov 13 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.1-1
- Update to 1.7.1
- Remove AVCodecTag patch
- Add wxsvg-freeworld to the linker paths

* Wed Oct 15 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.0-3
- Add ffmpeg-devel and fix wxsvg-freeworld-devel BR
- Add patch to fix AVCodecTag conversion errors
- Update wxsvg-freeworld patch so dvdstyler can be built without wxsvg (and use
  only wxsvg-freeworld instead)

* Sat Sep 27 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.0-2
- Rebuild for wxsvg 1.0b11 with ffmpeg enabled

* Sat Sep 06 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.7.0-1
- Update to 1.7.0

* Sat Aug 16 2008 Stewart Adam <s.adam at diffingo.com> - 1:1.6.2-1
- Update to 1.6.2

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
