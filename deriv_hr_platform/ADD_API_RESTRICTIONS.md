# How to Add API Key Restrictions

## Step-by-Step Guide (2 minutes)

### Step 1: Open Google Cloud Console API Credentials

Click this link:
👉 **https://console.cloud.google.com/apis/credentials**

(This will open in your browser)

---

### Step 2: Find Your API Key

Look for a key in the list that:
- Has a name like "API key" or "Browser key"
- Was created recently (today)
- Starts with `AIzaSyDhHx00OE...`

**What you'll see:**
```
API keys
┌─────────────────────────────────────────────────────┐
│ Name              Created      Restrictions          │
├─────────────────────────────────────────────────────┤
│ API key 1         Feb 8, 2026  None                 │ ← This one!
│ (Old) API key     Feb 7, 2026  Leaked (disabled)    │
└─────────────────────────────────────────────────────┘
```

---

### Step 3: Click the Pencil Icon (Edit)

On the right side of your API key row, you'll see three icons:
- 📋 Copy
- ✏️ Edit (Click this one!)
- 🗑️ Delete

**Click the ✏️ (Edit/Pencil) icon**

---

### Step 4: Scroll to "API restrictions"

You'll see a page titled "Edit API key". Scroll down to find:

```
API restrictions
○ Don't restrict key (currently selected)
● Restrict key ← Click this radio button!
```

**Click the "Restrict key" radio button**

---

### Step 5: Select ONLY "Generative Language API"

After clicking "Restrict key", a searchable list appears:

```
Search APIs...
☐ AI Platform Training & Prediction API
☐ Analytics Hub API
☐ BigQuery API
☐ Cloud Storage API
☐ Compute Engine API
...
☑ Generative Language API  ← Check ONLY this one!
...
☐ Maps JavaScript API
☐ Places API
```

**Type "Generative" in the search box to find it quickly**

**Check ONLY the box next to "Generative Language API"**

---

### Step 6: (Optional) Add Application Restrictions

Scroll up to the "Application restrictions" section:

```
Application restrictions
○ None (currently selected)
● HTTP referrers (web sites) ← Click this!
○ IP addresses
○ Android apps
○ iOS apps
```

**Click "HTTP referrers (web sites)"**

Then click **"ADD AN ITEM"** and enter:
```
https://deriv-hr-platform-520393715152.africa-south1.run.app/*
```

**Click Done**

---

### Step 7: Save

Scroll to the bottom of the page and click:

**[SAVE]** button (blue button)

---

## ✅ Verification

After saving, you should see:

```
API restrictions: Generative Language API
Application restrictions: HTTP referrers
```

---

## 🧪 Test It Still Works

After adding restrictions, wait 1-2 minutes, then test:

```bash
curl https://deriv-hr-platform-520393715152.africa-south1.run.app/api/health
```

**Expected response:**
```json
{
  "status": "ok",
  "agent": true,
  "tools": 12,
  "model": "gemini-2.5-flash"
}
```

If it works, you're done! 🎉

---

## ⚠️ Troubleshooting

### If you see "API key not valid"

**Wait 2-5 minutes** - restrictions can take a moment to propagate.

### If it still doesn't work after 5 minutes

The HTTP referrer restriction might be too strict. Go back and:
1. Edit the API key again
2. Under "Application restrictions", select **"None"**
3. Keep only the "API restrictions" (Generative Language API)
4. Save

This still provides good security by limiting which APIs can be called.

---

## 🎯 What This Does

### API Restrictions (Required)
✅ Prevents the key from being used for ANY Google API except Generative Language
✅ Even if leaked, can't be used for Maps, Cloud Storage, etc.
✅ Limits potential damage/cost

### HTTP Referrer Restrictions (Optional)
✅ Only works from your specific Cloud Run URL
✅ Can't be used from localhost or other domains
✅ Extra layer of protection

---

## 🔒 Security Summary

**Before restrictions:**
- ❌ Key works with ALL Google APIs
- ❌ Key works from ANY website/application
- ❌ High risk if leaked

**After restrictions:**
- ✅ Key ONLY works with Generative Language API
- ✅ Key ONLY works from your Cloud Run URL (if you added referrer)
- ✅ Much safer even if exposed

---

## 📸 Visual Guide

Can't find something? Here's what each section looks like:

### The Edit Page Layout:
```
┌─────────────────────────────────────────────┐
│ Edit API key                         [SAVE] │
├─────────────────────────────────────────────┤
│                                             │
│ Name: API key 1                             │
│ Key: AIzaSyDhHx00OEVi9yTYNBk9p95Wgj... 🔒  │
│                                             │
│ Application restrictions                     │
│ ○ None                                      │
│ ● HTTP referrers (web sites)                │
│   ┌───────────────────────────────────────┐ │
│   │ https://deriv-hr-platform-.../*      │ │
│   └───────────────────────────────────────┘ │
│                                             │
│ API restrictions                             │
│ ○ Don't restrict key                        │
│ ● Restrict key                              │
│   ☑ Generative Language API                 │
│                                             │
│                          [SAVE]             │
└─────────────────────────────────────────────┘
```

---

## 🆘 Need Help?

If you're stuck at any step, let me know which step number and I'll help!

**Quick link again:** https://console.cloud.google.com/apis/credentials
