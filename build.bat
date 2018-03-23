
pushd src\imagius && (

    pyinstaller imagius.spec --noconfirm --workpath=../../build --distpath=../../dist
    popd
)
