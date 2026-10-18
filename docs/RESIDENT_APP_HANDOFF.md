# Mobile app to B2B dashboard

The app team owns resident UI, report creation/GPS/photo capture and rewards. Sofea/Jia own the B2B map/inbox and operational follow-up.

Current prototype input is seed_app_reports. No production intake API is shipped. The former web resident submission URL is retired.

Suggested future incoming record:

```json
{
  "external_report_id": "APP-12345",
  "reported_at": "2026-10-17T10:15:00+08:00",
  "category": "flood",
  "description": "Leaves are blocking the drain beside the path.",
  "latitude": 3.1792,
  "longitude": 101.5150,
  "photo_attachment_id": "authenticated-file-reference"
}
```

These coordinates are examples, not an actual incident. Categories: flood, wind, drought, heat.

The receiving backend must derive project/reporter identity from authenticated access, validate coordinates/project scope, make external_report_id idempotent, validate private attachments and set initial status Open. An app request must not grant corporate permissions, verification, assignment or rewards.

Location and photo are separate fields. Use GPS/user-selected coordinates, not image EXIF. Photos are re-encoded and EXIF is stripped. Use authenticated multipart or controlled private attachments rather than arbitrary remote image fetching.

B2B display: category pin; thumbnail inbox card; photo/location/status inspector; work-item assignment and activity; project counts. The future app return payload should contain resident-safe status fields rather than internal staff notes.

No native app connection, push, automatic dispatch, verified route navigation or sponsored voucher redemption is implemented here.
