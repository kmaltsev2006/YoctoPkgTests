import sys
try:
    import ldb
    print("LDB_MODULE_IMPORTED")
    try:
        ldb_ctx = ldb.Ldb()
        print("LDB_CONTEXT_CREATED")
    except Exception as e:
        print(f"LDB_CONTEXT_ERROR: {e}")
except ImportError as e:
    print(f"IMPORT_ERROR: {e}")
    sys.exit(1)
