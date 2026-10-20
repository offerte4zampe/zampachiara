# Offerte da fiutare

The site publishes a transparent pre-launch newsletter section. It does not collect email addresses yet. Weekly drafts are prepared in ChatGPT; nothing is automatically sent to subscribers.

## Activate with Brevo

1. Create or connect the owner's Brevo account. Complete provider terms, sender verification and domain authentication with the owner. No passwords or API keys in GitHub.
2. Create a dedicated newsletter list, hosted subscription form and double opt-in confirmation email. Use a separate, unchecked consent checkbox specifying newsletter and promotional content from Offerte a 4 Zampe. Keep proof of consent and confirmation in Brevo.
3. Confirm and test the unsubscribe mechanism, including suppression of unsubscribed addresses. Do not import purchased, scraped or unconfirmed addresses.
4. Complete the site's privacy notice with the actual controller, provider, retention and relevant disclosures before accepting subscriptions. Set tracking preferences conservatively; newsletter consent is not automatic consent to individual tracking.
5. Enter the HTTPS hosted form URL (sibforms.com) into `site/data/newsletter.json`. Set DOI, unsubscribe, privacy notice, separate consent and provider-permission verification flags true **only after** each requirement has documented evidence. Any email test needs explicit sending authorization and an address controlled by the owner. The client rejects other hosts and incomplete configuration. See [the activation handoff](development/notification-activation.md): the planner and SQL schema are prepared offline, with no active collection, delivery adapter, remote database or schedule.
6. Update the homepage, newsletter page, metadata and privacy notice from preparation to active, without claiming unavailable coupons. Publish and verify the hosted form end to end.
7. Each campaign must contain sender identity and Brevo's functional unsubscribe link. Preview mobile/desktop and test before sending. Never put subscriber exports in the repository.

## Editorial template

Subject: Offerte da fiutare — [date/topic]
Preheader: [specific useful promise, without invented discounts]

- 3–5 offers: exact product, recipe, variant/quantity, shop, current price, date, shipping conditions and direct URL.
- Coupon section only when a current official source confirms code, eligible products, minimum spend, restrictions and expiry. Mark affiliate links if active.
- One practical comparison tip.
- Unsubscribe link and required sender information.

Avoid best-price claims, unverified recipe equivalence, fake urgency, medical advice and automatically ranking suspicious reference-price discounts. A draft is not authorization to dispatch a campaign.
