# image-regression-notification

## description

This action will test the image regression between the two specified URLs(`BASE_URL`, `COMPARE_URL`)

## usage
```yaml
- uses: ./
  with:
    BASE_URL: https://example.com
    COMPARE_URL: https://test.example.com
    SLACK_TOKEN: ${{ secrets.SLACK_TOKEN }}
    SLACK_CHANNEL: ${{ secrets.SLACK_CHANNEL }}
    ENABLE_SHOW_DIFF: false
```