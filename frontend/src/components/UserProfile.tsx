import React from 'react';
import {
  Box,
  Button,
  Typography,
  Card,
  CardContent,
  Avatar,
  Chip
} from '@mui/material';
import { User } from 'firebase/auth';

interface UserProfileProps {
  user: User;
  onSignOut: () => void;
}

export default function UserProfile({ user, onSignOut }: UserProfileProps) {
  return (
    <Card sx={{ maxWidth: 400, mx: 'auto', mt: 4 }}>
      <CardContent>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 2 }}>
          <Avatar
            src={user.photoURL || undefined}
            sx={{ width: 64, height: 64, mb: 2 }}
          >
            {user.displayName?.charAt(0) || user.email?.charAt(0)}
          </Avatar>
          <Typography variant="h6" component="h2" gutterBottom>
            {user.displayName || 'ユーザー'}
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {user.email}
          </Typography>
          <Chip
            label={user.emailVerified ? '認証済み' : '未認証'}
            color={user.emailVerified ? 'success' : 'warning'}
            size="small"
            sx={{ mt: 1 }}
          />
        </Box>

        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            UID: {user.uid}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            最終ログイン: {user.metadata.lastSignInTime}
          </Typography>
        </Box>

        <Button
          fullWidth
          variant="outlined"
          onClick={onSignOut}
          sx={{ mt: 2 }}
        >
          ログアウト
        </Button>
      </CardContent>
    </Card>
  );
}
