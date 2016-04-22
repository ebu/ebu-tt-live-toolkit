
try:
    from setuptools import setup
    extra = dict(test_suite="tests.test.suite", include_package_data=True, test_requires=[])
except ImportError:
    from distutils.core import setup
    extra = {}


packages=[
    "ebu_tt_live",
    "ebu_tt_live.bindings",
    "ebu_tt_live.clocks",
    "ebu_tt_live.scripts"
]


setup(
    name="ebu-tt-live",
    version="0.0.1",
    description="EBU-TT Part 3 library implementing Specification EBU-3370",
    install_requires=[
        "PyXB",
        "ipdb"  # This will eventually be removed from here
    ],
    license="BSD3",
    packages=packages,
    entry_points={
        'console_scripts': [
            'ebu-dummy-encoder = ebu_tt_live.scripts.ebu_dummy_encoder:main',
            'ebu-interactive-shell = ebu_tt_live.scripts.ebu_interactive_shell:main'
        ]
    }
)