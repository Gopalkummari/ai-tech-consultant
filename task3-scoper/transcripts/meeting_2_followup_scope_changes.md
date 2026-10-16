# Meeting Transcript 2: Follow-Up & Scope Revision Call
**Client**: Apex Legal Directory  
**Date**: October 15, 2026 • 2:30 PM EST  
**Participants**:
- **Arthur Dent** (Founder & CEO, Apex Legal)
- **Trillian Astra** (Product Lead, Apex Legal)
- **Jordan Miller** (Senior AI Tech Consultant, Brilliant Directories Partner Agency)

---

**Jordan Miller (Consultant)**: Welcome back Arthur and Trillian. I've sent over the preliminary architecture. Today let's review the adjustments you mentioned over email, identify what has changed, and update our scope and quotation.

**Arthur Dent (Founder)**: Thanks Jordan. We reviewed our budget with our investors. We had a few important decisions:
First decision: We are **DROPPING the native iOS/Android mobile app** for phase 1. It adds too much cost and timeline risk. We tested the web version on iPhones and Android browsers, and it's plenty fast and mobile-responsive. Let's remove the mobile app from the current SOW.

**Jordan Miller**: That's a wise decision for phase 1. That saves you 70 hours of custom engineering and about $7,000 right off the top.

**Trillian Astra (Product Lead)**: Second change: On the Lead Distribution, in our first meeting we said a fixed 25-mile radius. However, in rural states like Wyoming or Montana, attorneys might be 60 miles away. So we want a **tiered radius expansion**: if no attorney is within 25 miles, expand automatically to 50 miles or statewide.

**Jordan Miller**: Understood. In BD, standard radius is a single fixed slider. To support automated fallback expansion, we can configure a lightweight custom webhook logic or tiered lead distribution rule. That will be classified as a Standard Customization (~4 hours).

**Arthur Dent**: Third requirement—this is completely NEW:
When a lead is matched, attorneys told us they miss emails. We need **automated instant SMS text messages** sent directly to the attorney's mobile phone using Twilio.

**Jordan Miller**: Excellent. That is a NEW item outside the original discovery scope. BD has an outbound Lead Webhook under Developer Tools >> Webhooks. We can connect that to a Twilio SMS function. We will quote that as an added change item: ~6 hours of integration and testing.

**Trillian Astra**: Fourth requirement—also NEW:
During registration, we cannot have fake attorneys. We need to collect:
1. State Bar License Number (mandatory text field)
2. Year of Admission to State Bar (numeric dropdown)
3. Law School Name (text input)
Can we add these to the standard signup form?

**Jordan Miller**: Yes! That falls under BD's Form Manager in Toolbox >> Form Manager >> Listing - Contact Details. We can add those custom fields, mark them required, and have them display on their public profile cards. That is a quick configuration task (~2 hours).

**Arthur Dent**: Fantastic. Finally, what is the impact on timeline? We want to launch in 2 weeks. Can we deliver this revised scope in 2 weeks?

**Jordan Miller**: Yes, by removing the 70-hour mobile app and replacing it with the Twilio SMS webhook and custom form fields, our total engineering effort dropped from ~110 hours to only ~28 hours! A 2-week launch is very achievable. I will produce a formal Scope Diff report, revised Task List, and final Proposal for your approval.
