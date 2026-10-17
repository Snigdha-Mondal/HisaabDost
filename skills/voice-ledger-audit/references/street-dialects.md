# Street Dialects & Colloquial Units Reference

This guide catalogs common linguistic expressions, units of measurement, and colloquial phrasing used by Indian street food stalls, tea stalls, and vegetable vendors.

---

## 1. Unit & Quantity Mapping

| Colloquial Unit | Standard Unit | Typical Commodity | Conversion / Value |
|---|---|---|---|
| *dabba* (डब्बा) | tin / can | Cooking oil, vanaspati, ghee | Standard 15L or 15kg commercial canister |
| *peti* (पेटी) | crate / wooden box | Tomatoes, apples, mangoes, eggs | Variable by commodity (e.g. 25kg tomatoes) |
| *paav* (पाव) | quarter kilogram | Spices, ginger, chillies, garlic | 250 grams (0.25 kg) |
| *aadha kilo* (आधा किलो) | half kilogram | Vegetables, sugar, tea powder | 500 grams (0.5 kg) |
| *sawa kilo* (सवा किलो) | 1.25 kg | Staples, flour, lentils | 1.25 kg |
| *dedh kilo* (डेढ़ किलो) | 1.5 kg | Staples, onions, potatoes | 1.5 kg |
| *dhai kilo* (ढाई किलो) | 2.5 kg | Staples, paneer, bulk goods | 2.5 kg |
| *mutthi* (मुट्ठी) | fistful | Fresh herbs, curry leaves, coriander | ~50 grams (informal unit) |
| *ladi* (लड़ी) | hanging strip | Shampoo packets, pan masala, biscuits | 10 to 12 retail sachets |
| *bora* / *katta* (बोरा / कट्टा) | sack / gunny bag | Sugar, wheat flour (atta), potatoes, onions | 50 kg commercial bag |

---

## 2. Cash Register & Transaction Idioms

| Colloquial Phrase | Financial Category | Meaning |
|---|---|---|
| *galla* / *galle mein* / *daraaj* | `sales_revenue` | Cash register drawer / cash on hand |
| *aaj ki bikri* / *aaj ka dhandha* | `sales_revenue` | Today's gross cash turnover |
| *kharcha* / *laagat* | `expense` | Operational expenditure |
| *mandi se laaye* / *bazaar se kharida* | `expense` | Wholesale market inventory purchase |
| *udhaari* / *baaki khata* / *likha hua* | `customer_credit` | Informal customer tab / debt |
| *hath-udhaar* | `loan` | Hand loan / emergency borrowing |
| *bhada* / *rickshaw wala* | `expense (transport)` | Delivery or local transit cost |
| *thela lagane ka* / *chungi* | `expense (rent/permit)` | Stall positioning fee / municipal fee |

---

## 3. Ambiguity & Unbilled Delivery Protection

Street vendors frequently receive merchandise on informal consignment or late-billed deliveries:

1. **Unbilled Sample / Consignment**:
   - *Example*: *"Naya bakery wala 4 bread ke packet sample deke gaya"*
   - *Rule*: Record quantity (4 packets), description ("Sample bread"), but set `cost = 0.0`.
   - *Rationale*: Charging the vendor cash out-of-pocket when no money left the register creates an artificial book deficit.

2. **Pending Invoice / Deferred Settlement**:
   - *Example*: *"Supplier dudh de gaya, bola bill somvaar ko aayega"*
   - *Rule*: Record quantity and item name, flag status as `pending_invoice`. Do NOT deduct estimated cash from daily sales.

3. **Combined Outflows (Labor + Tea)**:
   - *Example*: *"Chhotu ko 150 diya aur chai ka 30"*
   - *Rule*: Split into two distinct line items:
     - Worker allowance / wages: ₹150
     - Staff tea expense: ₹30
