public with sharing class WeatherController {
    @AuraEnabled(cacheable=true)
    public static Weather__c getWeatherData() {
        List<Weather__c> records = [
            SELECT Id, Temperature__c, Description__c, City__c, Humidity__c, ObservedAt__c
            FROM Weather__c
            ORDER BY ObservedAt__c DESC
            LIMIT 1
        ];
        return records.isEmpty() ? null : records[0];
    }
}