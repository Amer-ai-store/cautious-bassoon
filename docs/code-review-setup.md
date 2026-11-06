# إعداد مراجعة Claude لطلبات السحب — cautious-bassoon

**المستودع الصحيح:** [Amer-ai-store/cautious-bassoon](https://github.com/Amer-ai-store/cautious-bassoon).
لا تعتمد على تعليمات أو أسرار المستودع الآخر `Amer-ai-store/Mohammad-Ahmed-Ghannam`: أسرار GitHub Actions منفصلة لكل مستودع، ولا تنتقل مع النسخ أو الدمج.

## لماذا فشلت المهمة 42104481073؟

في [المهمة 127538202765](https://github.com/Amer-ai-store/cautious-bassoon/actions/runs/42104481073/job/127538202765) فشلت خطوة `Require Claude authentication` قبل تشغيل Claude: لم يكن أيّ من `CLAUDE_CODE_OAUTH_TOKEN` أو `ANTHROPIC_API_KEY` متاحًا في **هذا المستودع**. هذه نتيجة مصادقة وليست فشل مراجعة للكود أو مشكلة في Ubuntu. ومن غير المقبول جعل الفحص ناجحًا دون إجراء مراجعة حقيقية.

## خطوة الإعداد المطلوبة (اعتماد واحد)

افتح [إعدادات أسرار Actions لهذا المستودع](https://github.com/Amer-ai-store/cautious-bassoon/settings/secrets/actions) واختر **New repository secret**، ثم استخدم إحدى الطريقتين:

1. **مفتاح Anthropic API:** أنشئ مفتاحًا صالحًا من [Anthropic Console](https://console.anthropic.com/settings/keys) واحفظه تحت الاسم `ANTHROPIC_API_KEY`. يشترط أن تكون صلاحية النموذج والرصيد متاحين. اشتراك ChatGPT أو Claude Pro ليس رصيدًا تلقائيًا لـ Anthropic API.
2. **رمز اشتراك Claude Code:** من بيئة Linux أو macOS أو Windows تدعم Claude Code، شغّل `claude setup-token` واحفظ الرمز الكامل الخاص بالاشتراك كسر `CLAUDE_CODE_OAUTH_TOKEN`. على الهاتف يمكن استخدام Codespaces **إن كان متاحًا في حسابك**؛ قد تتطلب الخدمة حصة أو تكلفة إضافية. بعد فتح Codespace من **هذا المستودع**، شغّل `bash scripts/save-claude-token.sh`؛ سيُنشئ السكربت الرمز، ويختبره عبر Claude، ويحفظه في `Amer-ai-store/cautious-bassoon` حصريًا بعد التحقق من عنوان مستودع Git.

**السلامة:** لا تضع الرمز أو المفتاح في رسالة أو Issue أو ملف متعقب أو صورة. لا تعرض السر في سجلات عامة. لا تستعمل رموز مصادقة منتهية أو مقتطعة. لا يزيل السكربت أسرارًا موجودة تلقائيًا؛ وإذا كان `ANTHROPIC_API_KEY` موجودًا مع رمز OAuth فإن Workflow الحالي **يفضّل مفتاح API**. إذا أردت استخدام الاشتراك، تحقق أولًا من عدم حاجة أي وظيفة أخرى إلى مفتاح API، ثم أزله من واجهة إعدادات الأسرار بنفسك.

## التحقق الفعلي بعد الإعداد

- افتح Pull Request جديدًا غير Draft (أو ادفع تعديلًا إلى PR مفتوح) لتشغيل `.github/workflows/claude-code-review.yml`.
- يجب نجاح `Require Claude authentication` أو تخطيها لوجود السر، ثم `Prepare the Claude token` و`Review the pull request` بحسب مسار المصادقة.
- تحقق من ظهور مراجعة Claude الحقيقية على PR، ومن انتهاء وظيفة `review` بـ `success`. وجود اسم السر وحده لا يثبت صلاحيته.
- سجّل رابط التشغيل الجديد والنتيجة. إذا فشل الإجراء، شخّص رسالة الخطأ دون كشف أي سر. لا تعِد وصف المهمة `42104481073` القديمة بأنها ناجحة: كان PR #2 مدموجًا بالفعل قبل المحاولة الثالثة.
- لا تُفعّل نشر الإنتاج لإصلاح مراجعة Claude. النشر مُجمّد بموجب Issue #102، وفحص المراجعة مستقل عنه.

**الحالة حتى نجاح التشغيل الحقيقي:** `BLOCKED — CLAUDE REVIEW NOT VERIFIED`.
