javac -cp ".:$(pwd)/lib/*" EntryPoint.java #ChangeCounterAdapter.java TypedChangeCounterAdapterFactory.java
echo compiled
python updateManifest.py
jar cfm EntryPoint.jar manifest.mf EntryPoint.class #ChangeCounterAdapter.class TypedChangeCounterAdapterFactory.class TypedChangeCounterAdapterFactory$1.class
echo jar created
