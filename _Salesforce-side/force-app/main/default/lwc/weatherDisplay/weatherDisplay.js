import { LightningElement, wire } from 'lwc';
import getWeatherData from '@salesforce/apex/weatherController.getWeatherData';


export default class WeatherDisplay extends LightningElement {
        record;
        error;
        // This component will display weather data
        // Fetch weather data from Apex controller
        @wire(getWeatherData)
        wiredWeather({ data, error }) {
        if (data) {
            this.record = data;
            this.error = undefined;
            console.log('[wire] data =', JSON.stringify(this.record));

        } else if (error) {
            this.error = error;
            this.record = undefined;
            console.error('[wire] error =', JSON.stringify(error));
        }
    }

    get hasData() {
        return !!this.record;
    }

    // Примеры геттеров для удобства шаблона
    get temperature() { return this.record?.Temperature__c; }
    get condition()   { return this.record?.Description__c; }
    get city()        { return this.record?.City__c; }
    get humidity()    { return this.record?.Humidity__c; }
    get observedAt()  { return this.record?.ObservedAt__c; } // ISO-строка

    connectedCallback() {
        console.log('Weather Data:', this.record);
        console.log('Weather error:', this.error);
    }
    renderedCallback() {
        console.log('Weather Data:', this.record);
        console.log('Weather error:', this.error);
        // You can access the data via this.record.data and errors
    }


}