# Maintainer: Timothy Brown <sysop@timb.us>

pkgname=raspberrypi-bluetooth
pkgver=1.0.0
pkgrel=2
pkgdesc="Provides Bluetooth support for Raspberry Pi 3B/3B+/ZeroW without using legacy Bluez tools."
arch=('armv6h' 'armv7h' 'aarch64')
url="http://github.com/timothybrown/raspberrypi-bluetooth"
license=('MIT')
depends=('bluez' 'bluez-utils' 'python' 'python-systemd')
makedepends=('python-setuptools' 'python-wheel')
source=("$pkgname-$pkgver.py"
        "$pkgname-$pkgver.service"
        "git+https://github.com/timothybrown/python-rpinfo.git")
md5sums=('15f8a2d3a1eb39a2568e03489fe2385b'
         '90674910d8a23d4ba7ca2bd068fb55a4'
         'SKIP')
build() {
	cd "$srcdir/python-rpinfo"
	python3 setup.py build
}
package() {
	cd "$srcdir/python-rpinfo"
	python3 setup.py install --root "$pkgdir"
	install -d "$pkgdir/usr/bin" "$pkgdir/usr/lib/systemd/system"
	install -m 755 "$srcdir/$pkgname-$pkgver.py" "$pkgdir/usr/bin/raspberrypi-bluetooth"
	install -m 644 "$srcdir/$pkgname-$pkgver.service" "$pkgdir/usr/lib/systemd/system/raspberrypi-bluetooth.service"
}