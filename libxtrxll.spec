%define commit 1b6eddfbedc700efb6f7e3c3594e43ac6ff29ea4
%define xtrx_group xtrx
%define sover   0
%define libname libxtrxll%{sover}
%define major 0
%define libname %mklibname xtrxll %{major}
%define devname %mklibname -d xtrxll

Name:           libxtrxll
Version:        0.0.0+git.20201202
Release:        1.3
Summary:        XTRX Low-level API library
License:        LGPL-2.1-only
Group:          Development/Libraries/C and C++
URL:            http://xtrx.io
#Git-Clone:     https://github.com/xtrx-sdr/libxtrxll.git
Source0:	https://github.com/xtrx-sdr/libxtrxll/archive/%{commit}.zip
Patch0:         libxtrxll-fix-udev-permissions.patch
BuildRequires:  cmake
BuildRequires:  git-core
BuildRequires:  pkgconfig(libusb)
BuildRequires:  pkgconfig(libusb3380)

%description
Low level XTRX hardware abstraction library.

%package -n %{libname}
Summary:        XTRX Low-level API library
Group:          System/Libraries
Requires:       xtrx-usb-udev

%description -n %{libname}
Low level XTRX hardware abstraction library.

%package -n	%{devname}
Summary:        XTRX Low-level API library - devel
Group:          Development/Libraries/C and C++
Requires:       %{libname} = %{EVRD}

%description -n	%{devname}
Low level XTRX hardware abstraction library.

This subpackage contains libraries and header files for developing
applications that want to make use of libxtrxll.

%package -n xtrxll-tools
Summary:        Low level tools for XTRX
Group:          Hardware/Other
Requires:	%{libname} = %{EVRD}

%description -n xtrxll-tools
Low level tools for XTRX SDR devices.

%package -n xtrx-usb-udev
Summary:        Udev rules for XTRX USB devices
Group:          Hardware/Other
Provides:       xtrx-udev = %{version}
Obsoletes:      xtrx-udev < %{version}
BuildArch:      noarch

%description -n xtrx-usb-udev
Udev rules for XTRX USB devices.

%prep
%setup -q -n %{name}-%{commit}

%build
export CFLAGS="%{optflags} -lusb-1.0"
%cmake \
%ifarch %{ix86} %{x86_64}
    -DFORCE_ARCH=x86_64 \
%endif
%ifarch %{arm} aarch64
    -DFORCE_ARCH=arm \
%endif
    -DENABLE_PCIE=ON \
    -DENABLE_USB3380=ON \
    -DINSTALL_UDEV_RULES=ON \
    -DUDEV_RULES_PATH=%{_udevrulesdir}
%make_build

%install
%make_install -C build
install -d %{buildroot}/%{_bindir}
mv %{buildroot}%{_libdir}/xtrxll/test_xtrxflash %{buildroot}/%{_bindir}
mv %{buildroot}%{_libdir}/xtrxll/test_xtrxll %{buildroot}/%{_bindir}

%post   -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig
%pre -n xtrx-usb-udev
getent group %{xtrx_group} >/dev/null || groupadd -r %{xtrx_group}

%files -n xtrx-usb-udev
%{_udevrulesdir}/50-xtrx.rules

%files -n %{libname}
%{_libdir}/libxtrxll.so.%{major}*

%files -n %{devname}
%license LICENSE
%doc README.md
%{_includedir}/xtrxll_*.h
%{_libdir}/libxtrxll.so
%{_libdir}/pkgconfig/libxtrxll.pc

%files -n xtrxll-tools
%{_bindir}/test_xtrxflash
%{_bindir}/test_xtrxll

%files -n xtrx-usb-udev
%{_udevrulesdir}/50-xtrx-usb3380.rules
