import Phaser from 'phaser';
import { Player } from '../entities/Player';
import { Enemy } from '../entities/Enemy';
import { RunState } from '../../state/RunState';
import { TelegramBridge } from '../../telegram/TelegramBridge';

export class GameScene extends Phaser.Scene {
  private player!: Player;
  private enemies!: Phaser.Physics.Arcade.Group;
  private bullets!: Phaser.Physics.Arcade.Group;
  private walls!: Phaser.Physics.Arcade.StaticGroup;
  private scoreText!: Phaser.GameObjects.Text;
  private killsText!: Phaser.GameObjects.Text;
  private nextShotAt = 0;
  private spawnTimer?: Phaser.Time.TimerEvent;

  constructor() {
    super('GameScene');
  }

  create(): void {
    RunState.reset();
    this.physics.world.setBounds(0, 0, 960, 600);
    this.cameras.main.setBackgroundColor('#071007');
    this.drawArena();

    this.walls = this.physics.add.staticGroup();
    this.createWall(480, 16, 960, 32);
    this.createWall(480, 584, 960, 32);
    this.createWall(16, 300, 32, 600);
    this.createWall(944, 300, 32, 600);
    this.createWall(290, 170, 360, 32);
    this.createWall(695, 390, 330, 32);

    this.player = new Player(this, 480, 320);
    this.enemies = this.physics.add.group({ runChildUpdate: false });
    this.bullets = this.physics.add.group({ runChildUpdate: false });

    this.physics.add.collider(this.player, this.walls);
    this.physics.add.collider(this.enemies, this.walls);
    this.physics.add.overlap(this.bullets, this.enemies, (bulletObject, enemyObject) => {
      this.onBulletEnemy(bulletObject as Phaser.Physics.Arcade.Image, enemyObject as Enemy);
    });
    this.physics.add.overlap(this.player, this.enemies, (_playerObject, enemyObject) => {
      this.onPlayerEnemy(enemyObject as Enemy);
    });

    this.createHud();
    this.spawnEnemy();
    this.spawnTimer = this.time.addEvent({ delay: 1350, loop: true, callback: () => this.spawnEnemy() });

    this.time.delayedCall(45_000, () => this.finishRun());
  }

  update(time: number): void {
    this.player.update(this.input.activePointer);
    this.enemies.getChildren().forEach(child => {
      const enemy = child as Enemy;
      if (enemy.active) enemy.chase(this.player);
    });

    if (time >= this.nextShotAt) {
      this.fire();
      this.nextShotAt = time + 125;
    }
  }

  private drawArena(): void {
    for (let x = 16; x < 960; x += 32) {
      for (let y = 16; y < 600; y += 32) this.add.image(x, y, 'floor').setAlpha(0.55);
    }
    this.add.text(52, 58, 'ACT I // LIQUIDITY ALLEY', {
      fontFamily: 'monospace', fontSize: '15px', color: '#25d5ff',
    }).setDepth(50);
  }

  private createWall(x: number, y: number, width: number, height: number): void {
    const wall = this.walls.create(x, y, 'wall') as Phaser.Physics.Arcade.Image;
    wall.setDisplaySize(width, height).refreshBody();
    wall.setTint(0x2c392c);
  }

  private createHud(): void {
    const panel = this.add.rectangle(810, 58, 250, 74, 0x050705, 0.88).setStrokeStyle(1, 0xc8ff28, 0.4).setDepth(70);
    this.scoreText = this.add.text(705, 38, 'SCORE 0', { fontFamily: 'monospace', fontSize: '16px', color: '#f5f7ef' }).setDepth(71);
    this.killsText = this.add.text(705, 64, 'KILLS 0', { fontFamily: 'monospace', fontSize: '16px', color: '#c8ff28' }).setDepth(71);
    panel.setScrollFactor(0);
  }

  private spawnEnemy(): void {
    if (this.enemies.countActive(true) >= 12) return;
    const edge = Phaser.Math.Between(0, 3);
    const point = edge === 0 ? { x: 72, y: Phaser.Math.Between(80, 520) }
      : edge === 1 ? { x: 888, y: Phaser.Math.Between(80, 520) }
        : edge === 2 ? { x: Phaser.Math.Between(80, 880), y: 72 }
          : { x: Phaser.Math.Between(80, 880), y: 528 };
    const enemy = new Enemy(this, point.x, point.y);
    this.enemies.add(enemy);
  }

  private fire(): void {
    const pointer = this.input.activePointer.positionToCamera(this.cameras.main) as Phaser.Math.Vector2;
    const angle = Phaser.Math.Angle.Between(this.player.x, this.player.y, pointer.x, pointer.y);
    const bullet = this.physics.add.image(
      this.player.x + Math.cos(angle) * 26,
      this.player.y + Math.sin(angle) * 26,
      'bullet',
    );
    bullet.setDepth(18);
    bullet.setCircle(5);
    bullet.setVelocity(Math.cos(angle) * 690, Math.sin(angle) * 690);
    this.bullets.add(bullet);
    this.time.delayedCall(900, () => bullet.active && bullet.destroy());
  }

  private onBulletEnemy(bullet: Phaser.Physics.Arcade.Image, enemy: Enemy): void {
    if (!bullet.active || !enemy.active) return;
    bullet.destroy();
    TelegramBridge.hit();

    this.cameras.main.shake(45, 0.0025);
    if (!enemy.damage()) return;

    RunState.addKill(enemy.points);
    TelegramBridge.kill();
    this.burst(enemy.x, enemy.y);
    enemy.destroy();
    this.scoreText.setText(`SCORE ${RunState.score.toLocaleString()}`);
    this.killsText.setText(`KILLS ${RunState.kills}`);
  }

  private onPlayerEnemy(enemy: Enemy): void {
    if (!enemy.active) return;
    enemy.destroy();
    this.cameras.main.flash(80, 255, 43, 145, false);
    this.cameras.main.shake(120, 0.008);
    this.finishRun();
  }

  private burst(x: number, y: number): void {
    for (let i = 0; i < 10; i += 1) {
      const shard = this.add.rectangle(x, y, Phaser.Math.Between(4, 10), Phaser.Math.Between(4, 10), 0xff2b91).setDepth(30);
      const angle = Phaser.Math.FloatBetween(0, Math.PI * 2);
      const distance = Phaser.Math.Between(35, 90);
      this.tweens.add({
        targets: shard,
        x: x + Math.cos(angle) * distance,
        y: y + Math.sin(angle) * distance,
        alpha: 0,
        angle: Phaser.Math.Between(-180, 180),
        duration: Phaser.Math.Between(220, 420),
        ease: 'Quad.out',
        onComplete: () => shard.destroy(),
      });
    }
  }

  private finishRun(): void {
    if (!this.scene.isActive()) return;
    this.spawnTimer?.remove(false);
    const snapshot = RunState.finish();
    this.scene.start('ResultScene', snapshot);
  }
}
