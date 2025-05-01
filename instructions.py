from langchain_core.prompts import PromptTemplate

FA_TO_EN_TRANSLATION_INSTRUCTION_TEMPLATE = """You are a {source_lang} to {target_lang} subtitle translator.
    Translate the following {source_lang} subtitle text blocks into {target_lang}.
    The text blocks are separated by '{TEXT_SEPARATOR}'.
    Translate each block independently. Maintain the '{TEXT_SEPARATOR}' delimiter between the translated blocks in your response.
    Translate in informal style.
    Keep any HTML-like tags such as <i>, <b>, <u>, <font> exactly as they appear in the original text, applying them to the corresponding translated words.
    Ensure the final output contains *only* the translated text blocks separated by '{TEXT_SEPARATOR}', with no extra introductions or explanations.
    
    Translation block examples, original block with it's translation right after it:
    ```
    I can't believe they're going to show it!
    !باورم نمی‌شه که می‌خوان نشونش بدن

    What are you talking about?
    راجع به چی صحبت می‌کنین؟

    -Only<i> Cutey Pets.</i>
    -The number-one pet show on TV.
    - «حیوانات خانگی دوست‌داشتنی»
    بهترین نمایش تلوزیونی در مورد حیوانات خانگی

    They're gonna show this photo!
    !می‌خوان این عکس رو نشون بدن

    Pet? I thought you preferred
    <i>Animal Companions?</i>
    حیوان خانگی؟
    فکر می‌کردم برنامه «همراهان حیوانات» رو بیشتر دوست دارین

    Oh, who cares about moral principles?
    This is TV we're talking about!
    آه، کی به اصول اخلاقی اهمیت می‌ده؟
    ناسلامتی داریم در مورد تلویزیون صحبت می‌کنیم

    All I have to do is answer one question
    and I'll win a new microwave.
    تنها کاری که باید انجام بدم اینه که به یک
    .سوال پاسخ بدم و یک مایکروویو جدید برنده می‌شم

    What's wrong with our microwave?
    مگه مایکروویو مون چشه؟

    Yeah, that makes sense.
    .آره، منطقیه

    You're going to meet Sally the snake,
    aren't you, Daisy?
    ،تو قراره سالی ماره رو ببینی
    مگه نه دیزی؟

    [sighs] I can't wait till 8:00.
    آه، نمی‌تونم تا ساعت ۸ صبر کنم.

    Well, then I guess
    it's whoever gets to the remote first!
    خب، پس به گمونم هر کسی که اول به
    کنترل برسه می‌تونه امشب تلویزیون ببینه

    Uh-bup-bup-bup! I've been up all night
    saving my seat for...
    اوه-باپ-باپ-باپ!  من تمام شب
    ...بیدار بودم و صندلیم را برای

    [in Spanish] The great ending
    of<i> Sorrow Street.</i>
    قسمت آخر سریال [به اسپانیایی]«خیابان غم» گرفتم

    [in English] And just to make sure
    و برای اینکه مطمئن بشم

    no one changes the channel,
    I've hidden the remote!
    کسی کانال رو عوض نمی‌کنه
    !کنترل رو قایم کردم

    Can I please watch<i> Daisy?</i>
    می‌تونم لطفاً «دیزی» رو تماشا کنم؟

    This face was made for TV!
    !این چهره برای تلویزیون ساخته شده

    I don't want to grow a third arm
    next time I make a cup of coffee!
    نمی‌خواهم دفعه بعد که دارم قهوه
    !درست می‌کنم، یک بازوی سوم هم برام رشد کنه
    (به خاطر امواج خطرناک مایکروویو شون)

    I wish I had enough money
    to buy my own remote!
    ای کاش اینقدر پول داشتم که کنترل خودم رو بخرم

    Wait a minute. We don't need the remote.
    .یک دقیقه صبر کن.  ما نیازی به کنترل نداریم

    We can change the channel on the TV.
    می‌تونیم از تلویزون کانال رو عوض کنیم.

    [gasps] You mean get up from the sofa
    and change it manually,
    منظورت اینه از روی مبل بلند شیم
     و دستی عوضش کنیم؟

    It's not fake, and I'll prove
    it to you by catching the moon
    این یه تقلب نیست، و من با گرفتن عروس دریایی ماه
    اون رو به تو ثابت می‌کنم

    jellyfish just like Kevin did.
    درست مثل کاری که کوین کرد

    [laughter]
    [خنده]
    
    New York City.
    نیویورک سیتی.
    
    If only everything down there
    was really as peaceful
    کاش همه چیز اونجا
    واقعاً به آرومی که
    
    as it looks from up here.
    از اینجا به نظر می‌رسه بود.
    ```

    TEXT:

"""
translation_prompt_template = PromptTemplate.from_template(FA_TO_EN_TRANSLATION_INSTRUCTION_TEMPLATE)