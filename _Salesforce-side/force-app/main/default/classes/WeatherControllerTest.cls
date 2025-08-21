@isTest
public class WeatherControllerTest {
    @testSetup
    static void setupData() {
        Weather__c testWeather = new Weather__c(
            Temperature__c = 25,
            Description__c = 'Sunny',
            City__c = 'Valencia',
            Humidity__c = 40,
            ObservedAt__c = DateTime.now()
        );
        insert testWeather;
    }

    @isTest
    static void testGetWeatherDataReturnsRecord() {
        Weather__c result = WeatherController.getWeatherData();
        System.assertNotEquals(null, result, 'Должна быть возвращена запись');
        System.assertEquals('Valencia', result.City__c);
        System.assertEquals('Sunny', result.Description__c);
    }

    @isTest
    static void testGetWeatherDataReturnsNullIfNoRecords() {
        delete [SELECT Id FROM Weather__c];
        Weather__c result = WeatherController.getWeatherData();
        System.assertEquals(null, result, 'Если записей нет, должен быть возвращён null');
    }
}