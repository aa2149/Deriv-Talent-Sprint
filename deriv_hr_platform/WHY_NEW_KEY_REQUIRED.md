# Why You Need a New API Key

## ❌ Cannot Resume Leaked Key

Once Google marks an API key as "leaked," it's **permanently disabled**. This is a security feature that cannot be reversed, even with restrictions.

**Reasons:**
1. The leaked key may already be in use by malicious actors
2. It might be cached in web archives, GitHub history, or logs
3. Google's automated systems flag it permanently to prevent abuse

## ✅ Solution: Create New Key with Proper Security

### The Right Way (3 Steps)

#### 1. Create New API Key
```bash
# Go to: https://aistudio.google.com/apikey
# Click: "Create API Key"
# Copy the new key
```

#### 2. Add Restrictions IMMEDIATELY

**Option A: API Restrictions (Recommended)**
- Go to: https://console.cloud.google.com/apis/credentials
- Find your new key → Edit
- Under "API restrictions":
  - Select "Restrict key"
  - Check only: ✅ **Generative Language API**
  - Save

**Option B: Application Restrictions**
- **HTTP referrers**: Add your Cloud Run URL
  ```
  https://deriv-hr-platform-520393715152.africa-south1.run.app/*
  ```
- **IP addresses**: Add Cloud Run NAT IP ranges (if known)

**Option C: Both (Most Secure)**
- Apply both API restrictions AND application restrictions

#### 3. Deploy Securely

**Method 1: Automated Script (Easiest)**
```bash
./secure-setup.sh
```
This interactive script will:
- Guide you through creating the key
- Set up Secret Manager (recommended)
- Deploy securely
- Test everything

**Method 2: Secret Manager (Manual - More Secure)**
```bash
# Store key securely
echo -n "YOUR_NEW_KEY" | gcloud secrets create google-api-key \
  --replication-policy="automatic" \
  --data-file=-

# Grant Cloud Run access
PROJECT_NUMBER=$(gcloud projects describe project-e2052cb2-3225-4f64-ba3 --format="value(projectNumber)")
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run services update deriv-hr-platform \
  --region africa-south1 \
  --update-secrets="GOOGLE_API_KEY=google-api-key:latest,GEMINI_API_KEY=google-api-key:latest"
```

**Method 3: Environment Variables (Quick but Less Secure)**
```bash
gcloud run services update deriv-hr-platform \
  --region africa-south1 \
  --update-env-vars "GOOGLE_API_KEY=YOUR_NEW_KEY,GEMINI_API_KEY=YOUR_NEW_KEY"
```

---

## 🔒 Security Best Practices

### What Went Wrong?
Your key was leaked because:
1. ❌ It was in a local `.env` file
2. ❌ We showed it in shell scripts during debugging
3. ❌ It appeared in command outputs
4. ❌ No restrictions were applied

### How to Prevent This

#### ✅ DO:
1. **Use Secret Manager** for production
2. **Add API restrictions** immediately after creation
3. **Add application restrictions** (referrer/IP)
4. **Rotate keys** every 90 days
5. **Monitor key usage** in Google Cloud Console
6. **Use .gitignore** for .env files
7. **Use environment variables** in CI/CD pipelines

#### ❌ DON'T:
1. Commit keys to git
2. Share keys in plain text (Slack, email)
3. Log keys in application output
4. Use unrestricted keys in production
5. Hardcode keys in source code
6. Store keys in client-side code

---

## 📊 Comparison: Environment Variables vs Secret Manager

| Feature | Environment Variables | Secret Manager |
|---------|----------------------|----------------|
| **Security** | ⚠️ Visible in console | ✅ Encrypted, access-controlled |
| **Rotation** | ⚠️ Manual redeployment | ✅ Automatic version management |
| **Audit Logging** | ❌ No | ✅ Full audit trail |
| **Cost** | ✅ Free | ⚠️ ~$0.06 per 10,000 accesses |
| **Setup Time** | ✅ 1 minute | ⚠️ 3-5 minutes |
| **Best For** | Development/Testing | Production |

---

## 🚀 Quick Start

**Fastest way to fix everything:**

```bash
# Run the automated secure setup
cd /Users/ahmednawaz/Downloads/finallll/deriv_hr_platform
./secure-setup.sh
```

This script will:
1. ✅ Prompt you for a new API key
2. ✅ Help you add restrictions
3. ✅ Set up Secret Manager (optional)
4. ✅ Deploy securely
5. ✅ Test everything automatically

**Time required:** 3-5 minutes

---

## 🎯 Your Demo URL (Unchanged)

```
https://deriv-hr-platform-520393715152.africa-south1.run.app
```

The URL never changes - only the API key needs to be updated!

---

## 📖 References

- [API Key Best Practices](https://docs.cloud.google.com/docs/authentication/api-keys)
- [API Key Restrictions](https://docs.cloud.google.com/docs/authentication/api-keys#api_key_restrictions)
- [Secret Manager Guide](https://cloud.google.com/secret-manager/docs/overview)
- [Cloud Run Security](https://cloud.google.com/run/docs/securing/service-identity)

---

## ❓ FAQ

**Q: Can I just delete the restriction on my old key?**
A: No. Leaked keys are permanently disabled by Google's security systems.

**Q: How do I know if my new key is working?**
A: Run `./secure-setup.sh` and it will test automatically, or manually test:
```bash
curl https://deriv-hr-platform-520393715152.africa-south1.run.app/api/health
```
Should return: `{"status":"ok","agent":true,...}`

**Q: Will my demo URL change?**
A: No! Your URL remains the same: `https://deriv-hr-platform-520393715152.africa-south1.run.app`

**Q: Should I use Secret Manager or environment variables?**
A: For a demo, environment variables are fine. For production, use Secret Manager.

**Q: How do I clean up the leaked key from git history?**
A: If you committed it:
```bash
# For recent commits
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch hr_agent/.env" \
  --prune-empty --tag-name-filter cat -- --all

# For GitHub (after local cleanup)
git push origin --force --all
```

---

**Ready?** Run `./secure-setup.sh` to get started! 🚀
