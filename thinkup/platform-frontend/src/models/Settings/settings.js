class Settings {
  /**
   * Class used to manage overall user's settings, NOT PROJECT
   * @param {String} language
   * @param {Boolean} notifications
   * @param {Boolean} theme
   */

  constructor(language, notifications, theme) {
    this.language = language;
    this.notifications = notifications;
    this.theme = theme;
  }
}
