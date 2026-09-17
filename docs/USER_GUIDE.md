# ComplaintIQ - User Guide

Welcome to the AI Customer Complaint Resolution Center. This guide will help you navigate the system.

## Roles
- **Agent**: Can view complaints, generate AI drafts, edit drafts, and resolve complaints.
- **Manager**: Can do everything an Agent does, plus manage escalations and view performance analytics.
- **Admin**: Has full access, including managing the Knowledge Base and system settings.

## How to Create a Complaint
*(Usually, complaints flow in automatically via email/API, but manual creation is possible)*
1. Navigate to the **Complaints** dashboard.
2. Click **"New Complaint"**.
3. Fill in the customer details and the complaint description.
4. Click **Save**. The AI will automatically classify the complaint's severity and sentiment.

## How to Use the AI Assistant
1. Open a specific complaint from the dashboard.
2. In the "Response" section, click **"Generate AI Draft"**.
3. The system will search the Knowledge Base, analyze the complaint, and write a draft.
4. **Review the Draft**: The AI will list the internal documents it used as sources.
5. **Edit**: You can modify the text directly in the text box.
6. **Send**: Once satisfied, approve and send the response.

## How to Manage Escalations
Complaints flagged as "High" severity by the AI, or manually escalated by an agent, appear in the **Escalations** tab.
1. Managers should review this queue daily.
2. Open an escalated ticket, review the agent's notes, and provide an override decision or contact the customer directly.

## How to Upload Documents (Knowledge Base)
To make the AI smarter, provide it with your company policies.
1. Navigate to the **Knowledge Base** tab (Admin only).
2. Click **"Upload Document"**.
3. Select a PDF or text file containing return policies, terms of service, or FAQs.
4. Click **Upload**. The system will process and "memorize" the document. The AI will immediately start using this new information for future drafts.

## How to Read Analytics
1. Navigate to the **Analytics** tab.
2. **Volume Chart**: See how many complaints are arriving over time.
3. **Sentiment Distribution**: See the breakdown of angry, neutral, or happy customer interactions.
4. **Category Breakdown**: Identify systemic issues (e.g., if "Shipping Delays" spikes, you know where to investigate in the business).
