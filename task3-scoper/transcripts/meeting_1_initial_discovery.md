# Meeting Transcript 1: Initial Discovery Call
**Client**: Apex Legal Directory (National Attorney Directory)  
**Date**: October 12, 2026 • 10:00 AM EST  
**Participants**:
- **Arthur Dent** (Founder & CEO, Apex Legal)
- **Trillian Astra** (Product Lead, Apex Legal)
- **Jordan Miller** (Senior AI Tech Consultant, Brilliant Directories Partner Agency)

---

**Jordan Miller (Consultant)**: Good morning Arthur and Trillian! Great to connect. The goal of today's call is to understand your vision for Apex Legal Directory, detail what features you need for your launch, and determine how much of this can be solved using Brilliant Directories out-of-the-box settings versus where custom development is required.

**Arthur Dent (Founder)**: Thanks Jordan. In short, we're building a nationwide platform for licensed attorneys in the United States. We have about 4,000 attorneys lined up across 50 states. We need to get this live quickly without wasting tens of thousands of dollars on custom software from scratch.

**Trillian Astra (Product Lead)**: Exactly. We have a list of core requirements:
First, our homepage must look premium. We want a hero banner with our legal firm photography, and a search bar where clients can search by legal specialty—like Criminal Defense or Family Law—and by City or ZIP code.

**Jordan Miller**: That's straightforward. Brilliant Directories has a built-in Homepage Layout manager with 'Category + Location' search dropdowns.

**Trillian Astra**: Next, we need our social media presence—LinkedIn, Twitter/X, and Facebook—prominently linked in the header and footer. Some developers quoted us 10 hours of custom coding just to add those icons.

**Jordan Miller**: I can already tell you that is 100% native in Brilliant Directories under General Settings > Social Media tab. It takes 10 minutes to enter your profile URLs and toggle the header/footer icons on. You should not pay a dollar of custom engineering for that.

**Arthur Dent**: Wow, that's a huge relief already. Now, what about taxonomy? We have a spreadsheet with roughly 3,500 legal categories and sub-specialties. Can we upload those via CSV or will we be typing them manually?

**Jordan Miller**: BD includes a bulk CSV Category Importer under My Members > Member Categories. As long as your CSV columns match Top Category and Sub-Level, you can import up to 5,000 categories in a single batch.

**Trillian Astra**: Perfect. Now here's a bigger feature: Lead Distribution. When a prospective client submits a legal consultation inquiry, we want the system to automatically match and notify up to 3 attorneys whose office is within a 25-mile radius of the client's ZIP code, and who specialize in that legal category.

**Jordan Miller**: That is built into BD's Lead Generation engine under Settings > Lead Settings. You configure the radius slider to 25 miles, set 'Max Members per Lead' to 3, and turn on category auto-matching.

**Arthur Dent**: Now, what about payment processing? We want attorneys to pay an annual subscription of $499 via credit card. And if an attorney decides to cancel within our 14-day grace period, our operations team needs to be able to issue a refund directly.

**Jordan Miller**: BD connects natively to Stripe. Subscriptions renew automatically, and refunds can be issued with one click from Finance > Transaction History.

**Trillian Astra**: Lastly, Arthur mentioned wanting a native iOS and Android mobile app downloaded from the App Store with push notifications. What would that take?

**Jordan Miller**: That is where custom engineering comes in. Brilliant Directories is fully responsive for mobile browsers out-of-the-box, but a native iOS/Android binary with native Apple/Google push notification servers requires custom React Native or Flutter wrapper development and API synchronization. That is a significant investment—typically 60 to 80 hours.

**Arthur Dent**: Understood. Let's get an initial SOW and quote based on what we discussed today, and then we will review with our advisory board.

**Jordan Miller**: Will do Arthur. I'll run this through our technical team and provide a complete Scope of Work and proposal!
