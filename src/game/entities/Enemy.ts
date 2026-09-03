import Phaser from 'phaser';
import type { Player } from './Player';

export class Enemy extends Phaser.Physics.Arcade.Sprite {
  hp = 2;
  readonly points = 150;
  readonly speed = 92;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, 'bot');
    scene.add.existing(this);
    scene.physics.add.existing(this);
    this.setDepth(15);
    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setCircle(18, 6, 6);
  }

  chase(player: Player): void {
    this.scene.physics.moveToObject(this, player, this.speed);
    this.setRotation(Phaser.Math.Angle.Between(this.x, this.y, player.x, player.y) - Math.PI / 2);
  }

  damage(): boolean {
    this.hp -= 1;
    this.setTintFill(0xffffff);
    this.scene.time.delayedCall(45, () => this.active && this.clearTint());
    return this.hp <= 0;
  }
}
