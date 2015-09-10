# -*- mode: python -*-		
a = Analysis(['__init__.py'],            
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ftk_controller.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False, manifest='ftk_controller.exe.manifest' )

coll = COLLECT(exe,
               a.binaries,			   
               a.zipfiles,
               a.datas +  [('config.ini', 'config.ini', 'DATA'),
						   ('exit.png', 'exit.png', 'DATA'),
						   ('extensions.csv', 'extensions.csv', 'DATA'),
						   ('logging.json', 'logging.json', 'DATA')
						   ],
						 
               strip=None,
               upx=True,
               name='ftk_controller')
