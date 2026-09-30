# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in /Users/.../android-sdk/tools/proguard/proguard-android.txt
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
-keep class com.workchord.android.data.models.** { *; }
