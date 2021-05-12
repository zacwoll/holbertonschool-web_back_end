export default class Car {
  constructor(brand, motor, color) {
    this._brand = brand;
    this._color = color;
    this._motor = motor;
  }

  cloneCar() {
    return new this.constructor();
  }
}
