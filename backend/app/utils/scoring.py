"""ボーリングスコア計算ユーティリティ"""
from typing import List
from app.models.game import Frame, GameSchema, RollRequest


def calculate_score(game: GameSchema, roll: RollRequest) -> GameSchema:
    """ゲームスコアを計算"""
    frame_index = roll.frame_number - 1
    frame = game.frames[frame_index]
    
    # ロールを追加
    frame.rolls.append(roll.pin_count)
    
    # フレームの状態を更新
    _update_frame_status(frame, frame_index)
    
    # 全フレームのスコアを再計算
    _calculate_all_frame_scores(game)
    
    # ゲームの完了状態をチェック
    if _is_game_completed(game):
        game.status = "completed"
    
    return game


def _update_frame_status(frame: Frame, frame_index: int):
    """フレームの状態を更新"""
    if frame_index < 9:  # 1-9フレーム
        if len(frame.rolls) == 1 and frame.rolls[0] == 10:
            # ストライク
            frame.is_strike = True
            frame.is_completed = True
        elif len(frame.rolls) == 2:
            # 2投目完了
            frame.is_completed = True
            if sum(frame.rolls) == 10:
                frame.is_spare = True
    else:  # 10フレーム目
        if len(frame.rolls) == 1 and frame.rolls[0] == 10:
            # ストライク
            frame.is_strike = True
        elif len(frame.rolls) == 2:
            if sum(frame.rolls) == 10:
                frame.is_spare = True
            elif not frame.is_strike:
                frame.is_completed = True
        elif len(frame.rolls) == 3:
            frame.is_completed = True


def _calculate_all_frame_scores(game: GameSchema):
    """全フレームのスコアを計算"""
    total_score = 0
    
    for i, frame in enumerate(game.frames):
        if i < 9:  # 1-9フレーム
            frame_score = _calculate_frame_score(game, i)
            total_score += frame_score
            frame.score = total_score
        else:  # 10フレーム目
            frame_score = _calculate_tenth_frame_score(frame)
            total_score += frame_score
            frame.score = total_score
    
    game.total_score = total_score


def _calculate_frame_score(game: GameSchema, frame_index: int) -> int:
    """フレームスコアを計算（1-9フレーム）"""
    frame = game.frames[frame_index]
    score = sum(frame.rolls)
    
    if frame.is_strike:
        # ストライクボーナス：次の2投
        score += _get_next_two_rolls_score(game, frame_index)
    elif frame.is_spare:
        # スペアボーナス：次の1投
        score += _get_next_roll_score(game, frame_index)
    
    return score


def _calculate_tenth_frame_score(frame: Frame) -> int:
    """10フレーム目のスコアを計算"""
    return sum(frame.rolls)


def _get_next_two_rolls_score(game: GameSchema, frame_index: int) -> int:
    """次の2投のスコアを取得"""
    if frame_index >= 8:  # 9フレーム目以降は10フレーム目から取得
        tenth_frame = game.frames[9]
        if len(tenth_frame.rolls) >= 2:
            return tenth_frame.rolls[0] + tenth_frame.rolls[1]
        elif len(tenth_frame.rolls) >= 1:
            return tenth_frame.rolls[0]
        return 0
    
    next_frame = game.frames[frame_index + 1]
    if len(next_frame.rolls) >= 2:
        return next_frame.rolls[0] + next_frame.rolls[1]
    elif len(next_frame.rolls) == 1 and next_frame.is_strike:
        # 次のフレームがストライクの場合、さらに次のフレームの1投目を取得
        if frame_index + 2 < len(game.frames):
            next_next_frame = game.frames[frame_index + 2]
            if len(next_next_frame.rolls) >= 1:
                return next_frame.rolls[0] + next_next_frame.rolls[0]
        return next_frame.rolls[0]
    
    return 0


def _get_next_roll_score(game: GameSchema, frame_index: int) -> int:
    """次の1投のスコアを取得"""
    if frame_index >= 9:
        return 0
    
    next_frame = game.frames[frame_index + 1]
    if len(next_frame.rolls) >= 1:
        return next_frame.rolls[0]
    
    return 0


def _is_game_completed(game: GameSchema) -> bool:
    """ゲーム完了チェック"""
    if len(game.frames) < 10:
        return False
    
    last_frame = game.frames[9]  # 10フレーム目
    
    # 10フレーム目の特別ルール
    if last_frame.is_strike or last_frame.is_spare:
        # ストライクまたはスペアの場合、3投必要
        return len(last_frame.rolls) >= 3
    
    # 通常の場合、2投で終了
    return len(last_frame.rolls) >= 2


def create_initial_frames() -> List[Frame]:
    """初期フレームを作成"""
    frames = []
    for i in range(10):
        frames.append(Frame(
            number=i + 1,
            rolls=[],
            score=0,
            is_strike=False,
            is_spare=False,
            is_completed=False
        ))
    return frames
