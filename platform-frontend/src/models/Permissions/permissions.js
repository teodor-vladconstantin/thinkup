class Permissions {
  /**
   * Class used to manage role's permissions
   * @param {Map<String, Boolean>} perms
   */
  constructor(perms) {
    this.perms = perms;
  }

  getPerm() {
    return this.perms;
  }

  checkPerm(perm) {
    return this.perms.has(perm);
  }
}
